#!/usr/bin/env python3
"""
Report PDF/HTML Generator
Converte automaticamente i report Markdown in PDF o HTML con immagini

Uso:
    python report_pdf_generator.py                    # Converte tutti i report
    python report_pdf_generator.py final_analysis_report.md    # Converte un report specifico
    python report_pdf_generator.py --watch           # Monitora e converte automaticamente
    python report_pdf_generator.py --force           # Forza conversione di tutti i file

Nota: Genera PDF automaticamente, con fallback HTML se necessario
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from bs4 import BeautifulSoup

class ReportPDFGenerator:
    """Generatore di PDF per report Markdown"""

    def __init__(self, reports_dir: str = None, config_file: str = None):
        if reports_dir is None:
            raise ValueError("reports_dir è obbligatorio. Specificare il percorso della directory reports.")

        self.reports_dir = Path(reports_dir)
        self.figures_dir = self.reports_dir.parent / "figures"

        # Carica configurazione
        self.config = self.load_config(config_file)

        # Verifica che le directory esistano
        if not self.reports_dir.exists():
            raise FileNotFoundError(f"Directory reports non trovata: {self.reports_dir}")

        if not self.figures_dir.exists():
            print(f"⚠️  Directory figures non trovata: {self.figures_dir}")
            print("   Le immagini potrebbero non essere incluse nel PDF")

    def load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Carica la configurazione PDF da file YAML"""
        if config_file is None:
            # Cerca il file di configurazione nella stessa directory dello script
            script_dir = Path(__file__).parent
            config_file = script_dir / "pdf_config.yaml"

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ Configurazione caricata da: {config_file}")
            return config
        except FileNotFoundError:
            print(f"⚠️  File configurazione non trovato: {config_file}")
            print("   Verrà utilizzata la configurazione di default")
            return self.get_default_config()
        except Exception as e:
            print(f"⚠️  Errore nel caricamento della configurazione: {str(e)}")
            print("   Verrà utilizzata la configurazione di default")
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Restituisce la configurazione di default se il file non è trovato"""
        return {
            'page': {'size': 'A4', 'margin_top': '2cm', 'margin_bottom': '2cm',
                    'margin_left': '2cm', 'margin_right': '2cm'},
            'title_page': {'font_size': '36pt', 'color': '#0969da'},
            'content': {'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                       'font_size': '14px', 'color': '#24292f'},
            'images': {'max_width': '90%', 'max_height': '70vh'}
        }

    def generate_css_from_config(self) -> str:
        """Genera CSS dinamico basato sulla configurazione YAML"""
        c = self.config

        css_parts = []

        # CSS Reset e setup base
        if c.get('advanced', {}).get('css_reset', True):
            css_parts.append("""
            /* Reset e setup base */
            * {
                box-sizing: border-box;
            }
            """)

        # Body e contenuto principale
        css_parts.append(f"""
        body {{
            font-family: {c['content']['font_family']};
            font-size: {c['content']['font_size']};
            font-weight: {c['content']['font_weight']};
            line-height: {c['content']['line_height']};
            color: {c['content']['color']};
            max-width: {c['content']['max_width']};
            margin: {c['content']['margin']};
            padding: {c['content']['padding']};
        }}
        """)

        # Pagina titolo
        css_parts.append(f"""
        /* Pagina titolo - Prima pagina */
        .title-page {{
            page-break-after: always;
            display: {c['title_page']['display']};
            flex-direction: column;
            justify-content: {c['title_page']['justify_content']};
            align-items: {c['title_page']['align_items']};
            min-height: {c['title_page']['min_height']};
            text-align: {c['title_page']['text_align']};
            padding: {c['title_page']['padding']};
        }}

        .title-page h1 {{
            font-family: {c['title_page']['font_family']};
            font-size: {c['title_page']['font_size']};
            font-weight: {c['title_page']['font_weight']};
            color: {c['title_page']['color']};
            margin: {c['title_page']['margin']};
            line-height: {c['title_page']['line_height']};
        }}
        """)

        # Indice/Table of Contents
        css_parts.append(f"""
        /* Indice - Seconda pagina */
        .toc-page {{
            page-break-after: always;
        }}

        .toc-title {{
            font-family: {c['toc']['item_font_family']};
            font-size: {c['toc']['title_font_size']};
            font-weight: {c['toc']['title_font_weight']};
            color: {c['toc']['title_color']};
            margin-bottom: {c['toc']['title_margin_bottom']};
            text-align: {c['toc']['title_text_align']};
        }}

        /* Stile dell'indice */
        nav#TOC {{
            max-width: {c['toc']['max_width']};
            margin: {c['toc']['margin']};
        }}

        nav#TOC ul {{
            list-style: {c['toc']['list_style']};
            padding: {c['toc']['padding']};
        }}

        nav#TOC li {{
            font-family: {c['toc']['item_font_family']};
            font-size: {c['toc']['item_font_size']};
            font-weight: {c['toc']['item_font_weight']};
            margin: {c['toc']['item_margin']};
            line-height: {c['toc']['item_line_height']};
        }}

        nav#TOC a {{
            text-decoration: {c['toc']['link_text_decoration']};
            color: {c['toc']['link_color']};
        }}

        nav#TOC a:hover {{
            color: {c['toc']['link_hover_color']};
        }}
        """)

        # Contenuto principale
        css_parts.append(f"""
        /* Contenuto principale - Pagine successive */
        .main-content {{
            padding: {c['content']['padding']};
        }}
        """)

        # Immagini
        css_parts.append(f"""
        /* Immagini */
        img {{
            max-width: 100% !important;
            height: auto !important;
            page-break-inside: avoid;
        }}

        /* Limita le dimensioni delle immagini per PDF */
        img[src*="../figures/"] {{
            max-width: {c['images']['max_width']} !important;
            max-height: {c['images']['max_height']} !important;
            display: {c['images']['display']};
            margin: {c['images']['margin']};
            box-shadow: {c['images']['box_shadow']};
        }}
        """)

        # Headers
        css_parts.append(f"""
        /* Headers nel contenuto */
        h1, h2, h3, h4, h5, h6 {{
            font-family: {c['headers']['font_family']};
            color: {c['headers']['color']};
            margin-top: {c['headers']['margin_top']};
            margin-bottom: {c['headers']['margin_bottom']};
            font-weight: {c['headers']['font_weight']};
            line-height: {c['headers']['line_height']};
            page-break-after: {c['headers']['page_break_after']};
        }}
        """)

        # Headers specifici
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if level in c['headers']:
                css_parts.append(f"""
        {level} {{
            font-size: {c['headers'][level]['font_size']};
            margin-top: {c['headers'][level]['margin_top']};
        }}
                """)

        # Evita interruzioni di pagina negli headers
        css_parts.append("""
        /* Evita interruzioni di pagina negli headers */
        h1, h2, h3 {
            page-break-after: avoid;
        }
        """)

        # Testo e paragrafi
        css_parts.append(f"""
        /* Testo e paragrafi */
        p {{
            margin-bottom: {c['text']['paragraph_margin_bottom']};
            orphans: {c['text']['orphans']};
            widows: {c['text']['widows']};
        }}

        /* Liste */
        li {{
            margin-bottom: {c['text']['list_margin_bottom']};
            line-height: {c['text']['list_line_height']};
        }}

        ul, ol {{
            margin-bottom: {c['text']['paragraph_margin_bottom']};
        }}
        """)

        # Testo grassetto
        if 'bold_text' in c:
            css_parts.append(f"""
        /* Testo grassetto */
        strong, b {{
            font-family: {c['bold_text']['font_family']};
            font-size: {c['bold_text']['font_size']};
            font-weight: {c['bold_text']['font_weight']};
            color: {c['bold_text']['color']};
        }}
        """)

        # Didascalie figure
        if 'figure_captions' in c:
            css_parts.append(f"""
        /* Didascalie figure */
        figcaption {{
            font-family: {c['figure_captions']['font_family']};
            font-size: {c['figure_captions']['font_size']};
            font-weight: {c['figure_captions']['font_weight']};
            font-style: {c['figure_captions']['font_style']};
            color: {c['figure_captions']['color']};
            margin-top: {c['figure_captions']['margin_top']};
            margin-bottom: {c['figure_captions']['margin_bottom']};
        }}
        """)

        # Tabelle
        css_parts.append(f"""
        /* Tabelle */
        table {{
            border-collapse: {c['table']['border_collapse']};
            width: {c['table']['width']};
            margin: {c['table']['margin']};
            page-break-inside: {c['table']['page_break_inside']};
        }}

        th, td {{
            border: {c['table_cell']['border']};
            padding: {c['table_cell']['padding']};
            word-wrap: {c['table_cell']['word_wrap']}; /* Aggiunto per gestire testo lungo */
            font-size: {c['table_cell']['font_size']}; /* Aggiunto per consistenza */
        }}

        th {{
            background-color: {c['table_header']['background_color']};
            font-weight: {c['table_header']['font_weight']};
            color: {c['table_header']['color']};
        }}

        td {{
            color: {c['table_cell']['color']};
        }}
        """)

        # Codice
        css_parts.append(f"""
        /* Codice */
        code {{
            font-family: {c['code']['font_family']};
            background-color: {c['code']['background_color']};
            padding: {c['code']['padding']};
            border-radius: {c['code']['border_radius']};
            font-size: {c['code']['font_size']};
            color: {c['code']['color']};
        }}

        pre {{
            font-family: {c['pre']['font_family']};
            background-color: {c['pre']['background_color']};
            padding: {c['pre']['padding']};
            border-radius: {c['pre']['border_radius']};
            overflow-x: {c['pre']['overflow_x']};
            page-break-inside: {c['pre']['page_break_inside']};
            font-size: {c['pre']['font_size']};
            color: {c['pre']['color']};
        }}
        """)

        # Citazioni
        css_parts.append(f"""
        /* Citazioni */
        blockquote {{
            border-left: {c['blockquote']['border_left']};
            padding-left: {c['blockquote']['padding_left']};
            margin-left: {c['blockquote']['margin_left']};
            color: {c['blockquote']['color']};
            page-break-inside: {c['blockquote']['page_break_inside']};
        }}
        """)

        # Regole di pagina
        css_parts.append(f"""
        /* Regole di pagina */
        @page {{
            size: {c['page']['size']};
            margin: {c['page']['margin_top']} {c['page']['margin_right']} {c['page']['margin_bottom']} {c['page']['margin_left']};
        }}

        @page :first {{
            margin-top: 4cm;
        }}

        /* Footer con numero pagina */
        @page {{
            @bottom-center {{
                content: {c['footer']['content']};
                font-family: {c['content']['font_family']};
                font-size: {c['footer']['font_size']};
                font-weight: {c['content']['font_weight']};
                color: {c['footer']['color']};
            }}
        }}
        """)

        # Utility classes
        css_parts.append(f"""
        /* Utility */
        .page-break {{
            {c['utilities']['page_break']};
        }}

        .no-break {{
            {c['utilities']['no_break']};
        }}
        """)

        return "\n".join(css_parts)

    def get_markdown_files(self) -> List[Path]:
        """Trova tutti i file Markdown nella directory reports"""
        return list(self.reports_dir.glob("*.md"))

    def convert_to_pdf(self, md_file: Path, force: bool = False) -> bool:
        """
        Converte un file Markdown in PDF

        Args:
            md_file: File Markdown da convertire
            force: Forza la conversione anche se il PDF è più recente

        Returns:
            bool: True se la conversione è riuscita
        """
        if not md_file.exists():
            print(f"❌ File non trovato: {md_file}")
            return False

        pdf_file = md_file.with_suffix('.pdf')

        # Verifica se il PDF è più recente del Markdown
        if not force and pdf_file.exists():
            md_mtime = md_file.stat().st_mtime
            pdf_mtime = pdf_file.stat().st_mtime
            if pdf_mtime > md_mtime:
                print(f"⏭️  PDF già aggiornato: {pdf_file.name}")
                return True

        print(f"🔄 Conversione: {md_file.name} → {pdf_file.name}")

        try:
            # Prima converti MD in HTML temporaneo
            html_temp = self.reports_dir / f"{md_file.stem}.html"

            # Crea CSS personalizzato per PDF usando la configurazione
            css_temp = self.reports_dir / f"{md_file.stem}.css"
            css_content = self.generate_css_from_config()

            # Scrivi il CSS su file temporaneo
            with open(css_temp, 'w', encoding='utf-8') as f:
                f.write(css_content)

            # Comando pandoc per convertire MD in HTML
            cmd_html = [
                "pandoc",
                "--from=gfm",  # Specifica che l'input è GitHub Flavored Markdown
                str(md_file.resolve()),  # Usa percorsi assoluti
                "-o", str(html_temp.resolve()),
                "--standalone",
                "--toc",
                "--toc-depth=3",
                "--css", str(css_temp.resolve()),
                "--variable", "pagetitle=" + md_file.stem.replace('_', ' ').title()
            ]

            # Esegui il comando dalla directory del progetto per garantire che i percorsi relativi delle immagini funzionino
            project_root = self.reports_dir.parent.parent
            result_html = subprocess.run(cmd_html, capture_output=True, text=True, cwd=project_root)

            if result_html.returncode != 0:
                print(f"❌ Errore nella conversione HTML di {md_file.name}")
                print(f"   Errore: {result_html.stderr}")
                return False

            # Post-processa l'HTML per aggiungere la struttura di pagina
            self._add_page_structure_beautifulsoup(html_temp, md_file)

            # Ora converti HTML in PDF usando un metodo alternativo
            # Usa wkhtmltopdf se disponibile, altrimenti prova con altri metodi
            pdf_success = False

            # Metodo 1: Prova con weasyprint se disponibile
            try:
                import os
                import weasyprint
                from weasyprint import HTML

                # Imposta DYLD_LIBRARY_PATH per macOS
                if os.name == 'posix' and os.uname().sysname == 'Darwin':
                    lib_path = '/opt/homebrew/lib'
                    current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
                    if lib_path not in current_dyld:
                        os.environ['DYLD_LIBRARY_PATH'] = f"{lib_path}:{current_dyld}"

                HTML(str(html_temp)).write_pdf(str(pdf_file))
                pdf_success = True
                print(f"✅ PDF generato con WeasyPrint: {pdf_file.name}")
            except (ImportError, Exception) as e:
                print(f"⚠️  WeasyPrint non disponibile o errore: {str(e)[:100]}...")
                pass

            # Metodo 2: Fallback - mantieni HTML per conversione manuale
            if not pdf_success:
                print(f"📄 HTML generato: {html_temp.name}")
                print(f"   💡 Per convertire in PDF:")
                print(f"      • Apri {html_temp} nel browser")
                print(f"      • Salva come PDF (Ctrl/Cmd+P → Salva come PDF)")
                print(f"      • O usa: pandoc {html_temp.name} -o {pdf_file.name}")
                return False  # Ritorna False ma il file HTML è stato creato

            # Rimuovi file temporanei se PDF è stato creato
            if pdf_success:
                try:
                    # if html_temp.exists():
                    #     html_temp.unlink()
                    # if css_temp.exists():
                    #     css_temp.unlink()
                    pass # Manteniamo i file temporanei per il debug
                except Exception as e:
                    print(f"⚠️  Impossibile rimuovere file temporanei: {str(e)}")

            return pdf_success

        except Exception as e:
            print(f"❌ Errore durante la conversione di {md_file.name}: {str(e)}")
            return False

    def _add_page_structure_beautifulsoup(self, html_file: Path, md_file: Path) -> None:
        """
        Aggiunge la struttura di pagina al file HTML generato usando BeautifulSoup.
        """
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Estrai il titolo dal nome del file
            title_text = md_file.stem.replace('_', ' ').title()
            
            if soup.body:
                # 1. Crea la pagina del titolo
                title_page_div = soup.new_tag('div', attrs={'class': 'title-page'})
                title_h1 = soup.new_tag('h1')
                title_h1.string = title_text
                title_page_div.append(title_h1)
                
                # 2. Aggiungi la classe 'main-content' al body
                soup.body['class'] = soup.body.get('class', []) + ['main-content']

                # 3. Gestisci il sommario (TOC)
                toc_nav = soup.find('nav', id='TOC')
                if toc_nav:
                    toc_page_div = soup.new_tag('div', attrs={'class': 'toc-page'})
                    toc_title_h1 = soup.new_tag('h1', attrs={'class': 'toc-title'})
                    toc_title_h1.string = "Indice"
                    
                    # Estrai il nav e mettilo dentro il nuovo div
                    toc_nav.extract() 
                    toc_page_div.append(toc_title_h1)
                    toc_page_div.append(toc_nav)
                    
                    # Inserisci il div del sommario e il div del titolo all'inizio del body
                    soup.body.insert(0, toc_page_div)
                    soup.body.insert(0, title_page_div)
                else:
                    # Se non c'è sommario, inserisci solo la pagina del titolo
                    soup.body.insert(0, title_page_div)
            
            # Scrivi il file HTML modificato
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"✅ Struttura pagina aggiunta a {html_file.name}")

        except Exception as e:
            print(f"⚠️  Impossibile aggiungere struttura pagina con BeautifulSoup: {str(e)}")


    def _add_page_structure(self, html_file: Path, md_file: Path) -> None:
        """
        DEPRECATO: Mantenuto per compatibilità, ma usare _add_page_structure_beautifulsoup
        """
        print("Funzione _add_page_structure deprecata, usare la versione BeautifulSoup.")
        pass

    def convert_all_reports(self, force: bool = False) -> None:
        """Converte tutti i report Markdown in PDF"""
        print("🔄 Conversione di tutti i report Markdown in PDF")
        print("=" * 60)

        md_files = self.get_markdown_files()
        if not md_files:
            print("❌ Nessun file Markdown trovato nella directory reports")
            return

        print(f"📄 Trovati {len(md_files)} file Markdown:")
        for md_file in md_files:
            print(f"   • {md_file.name}")
        print()

        converted = 0
        failed = 0

        for md_file in md_files:
            if self.convert_to_pdf(md_file, force):
                converted += 1
            else:
                failed += 1

        print("\n" + "=" * 60)
        print(f"📊 Risultati conversione:")
        print(f"   ✅ Convertiti: {converted}")
        print(f"   ❌ Falliti: {failed}")
        print(f"   📁 Directory: {self.reports_dir}")

    def watch_and_convert(self) -> None:
        """Monitora i file Markdown e converte automaticamente quando cambiano"""
        print("👀 Modalità monitoraggio attivata")
        print("   Premi Ctrl+C per interrompere")
        print("=" * 60)

        # Traccia l'ultimo tempo di modifica per ogni file
        last_modified = {}
        md_files = self.get_markdown_files()

        for md_file in md_files:
            last_modified[md_file] = md_file.stat().st_mtime
            print(f"📄 Monitoraggio: {md_file.name}")

        print("\n🔄 In attesa di modifiche...")

        try:
            while True:
                time.sleep(1)  # Controlla ogni secondo

                for md_file in md_files:
                    if not md_file.exists():
                        continue

                    current_mtime = md_file.stat().st_mtime
                    if current_mtime > last_modified[md_file]:
                        print(f"\n📝 Modifica rilevata: {md_file.name}")
                        self.convert_to_pdf(md_file, force=True)
                        last_modified[md_file] = current_mtime

        except KeyboardInterrupt:
            print("\n\n👋 Monitoraggio interrotto dall'utente")
            print("   I PDF sono stati mantenuti aggiornati fino all'ultimo controllo")

def main():
    parser = argparse.ArgumentParser(
        description="Converte report Markdown in PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:
  python report_pdf_generator.py                    # Converte tutti i report
  python report_pdf_generator.py final_analysis_report.md    # Converte un report specifico
  python report_pdf_generator.py --watch           # Monitora e converte automaticamente
  python report_pdf_generator.py --force           # Forza conversione di tutti i file
        """
    )

    parser.add_argument(
        'filename',
        nargs='?',
        help='Nome del file Markdown da convertire (senza estensione .md)'
    )

    parser.add_argument(
        '--watch', '-w',
        action='store_true',
        help='Monitora i file e converte automaticamente quando cambiano'
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Forza la conversione anche se il PDF è più recente'
    )

    parser.add_argument(
        '--reports-dir',
        help='Directory dei report (default: ../reports dalla posizione dello script)'
    )

    parser.add_argument(
        '--config-file',
        help='File di configurazione YAML (default: pdf_config.yaml nella directory degli script)'
    )

    args = parser.parse_args()

    try:
        generator = ReportPDFGenerator(args.reports_dir, args.config_file)

        if args.watch:
            generator.watch_and_convert()
        elif args.filename:
            # Converti un file specifico
            md_file = generator.reports_dir / f"{args.filename}.md"
            success = generator.convert_to_pdf(md_file, args.force)
            sys.exit(0 if success else 1)
        else:
            # Converti tutti i file
            generator.convert_all_reports(args.force)

    except Exception as e:
        print(f"❌ Errore: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
