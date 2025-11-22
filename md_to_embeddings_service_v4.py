#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to Embeddings Service - ОНОВЛЕНА ВЕРСІЯ v4.3
Сервіс для перетворення markdown файлів в embeddings
Версія: 4.3.0 (З можливістю вказати цільову директорію)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json
from datetime import datetime

# Список сервісних файлів, які НЕ включаємо в результат
SERVICE_FILES = {
    'codetomd.py',
    'codetomd.bat', 
    'drakon_converter.py',
    'md_to_embeddings_service.py',
    'md_to_embeddings_service_v4.py',
    'md-to-embeddings-service.bat',
    'run_md_service.bat',
    'run_md_service.sh',
    '.gitignore',
    'package-lock.json',
    'yarn.lock',
    '.DS_Store',
    'Thumbs.db'
}

# Сервісні директорії для ігнорування
SERVICE_DIRS = {
    '.git', 
    'node_modules', 
    'venv', 
    '__pycache__', 
    '.vscode',
    '.idea', 
    'dist', 
    'build', 
    'target', 
    '.pytest_cache',
    'env',
    '.env'
}

# Глобальна змінна для збереження шляху до скрипта
SCRIPT_DIR = Path(__file__).parent.absolute()

def check_dependencies():
    """Перевіряє та встановлює необхідні залежності"""
    print("\n" + "🔍"*20)
    print("--- ПЕРЕВІРКА ЗАЛЕЖНОСТЕЙ ---")
    print("🔍"*20)
    
    required_packages = {
        'reportlab': 'reportlab'
    }
    
    missing_packages = []
    
    print("\n📦 Перевірка встановлених пакетів:")
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - не встановлено")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️ Виявлено відсутні пакети: {', '.join(missing_packages)}")
        install = input("\n❓ Встановити відсутні пакети? (y/n): ").strip().lower()
        
        if install == 'y':
            print("\n📥 Встановлення пакетів...")
            for package in missing_packages:
                try:
                    print(f"\n   Installing {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    print(f"   ✅ {package} встановлено успішно")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Помилка встановлення {package}: {e}")
                    return False
            
            print("\n✅ Всі залежності встановлено!")
            return True
        else:
            print("\n⚠️ Функції PDF будуть недоступні без необхідних пакетів.")
            return False
    else:
        print("\n✅ Всі необхідні пакети встановлено!")
        return True

def show_menu():
    """Показує головне меню програми"""
    print("\n" + "="*60)
    print("    🔧 MD TO EMBEDDINGS SERVICE v4.3 🔧")
    print("="*60)
    print("Виберіть варіант функціоналу:")
    print("1. 🚀 Розгорнути шаблон проєкту")
    print("2. 🔄 Конвертувати DRAKON схеми (.json → .md)")
    print("3. 📄 Створити узагальнюючий файл з коду проєкту")
    print("4. 📤 Копіювати файл до Dropbox/іншої директорії")
    print("5. 🚪 Вихід")
    print("="*60)

def get_target_directory():
    """Отримує цільову директорію для обробки"""
    print("\n" + "📁"*20)
    print("--- ВИБІР ДИРЕКТОРІЇ ДЛЯ ОБРОБКИ ---")
    print("📁"*20)
    
    current_dir = Path.cwd()
    print(f"\n📍 Поточна директорія скрипта: {SCRIPT_DIR}")
    print(f"📍 Робоча директорія: {current_dir}")
    
    print("\n📝 Оберіть варіант:")
    print("1. 📂 Використати поточну директорію")
    print("2. 🔍 Вказати іншу директорію (абсолютний або відносний шлях)")
    
    choice = input("\n👉 Ваш вибір (1-2, Enter для поточної): ").strip()
    
    if choice == "2":
        target_path = input("\n📂 Введіть шлях до директорії: ").strip()
        
        if not target_path:
            print("⚠️ Шлях не вказано, використовуємо поточну директорію")
            return current_dir
        
        # Розгортаємо ~ та відносні шляхи
        target_path = os.path.expanduser(target_path)
        target_dir = Path(target_path).resolve()
        
        if not target_dir.exists():
            print(f"\n❌ Директорія не існує: {target_dir}")
            return None
        
        if not target_dir.is_dir():
            print(f"\n❌ Це не директорія: {target_dir}")
            return None
        
        print(f"\n✅ Обрано директорію: {target_dir}")
        return target_dir
    else:
        print(f"\n✅ Використовуємо поточну директорію: {current_dir}")
        return current_dir

def option_1_deploy_template():
    """Варіант 1: Розгорнути шаблон проєкту"""
    print("\n" + "🚀"*20)
    print("--- ВАРІАНТ 1: Розгортання шаблону ---")
    print("🚀"*20)
    
    try:
        # Створюємо директорії
        directories = ["code", "drn", "srv"]
        print("📁 Створюємо директорії:")
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            print(f"   ✓ {directory}/")
        
        # Створюємо базові файли
        print("\n📄 Створюємо базові файли:")
        
        print("   📄 codetomd.py...")
        create_codetomd_file()
        print("   ✓ codetomd.py")
        
        print("   📄 drakon_converter.py...")
        create_drakon_converter_file()
        print("   ✓ drakon_converter.py")
        
        create_readme_files()
        
        print("\n✅ Шаблон проєкту успішно розгорнуто!")
        print("📋 Створено:")
        print("   - 📁 Директорії: code/, drn/, srv/")
        print("   - 📄 Файли: codetomd.py, drakon_converter.py")
        print("   - 📖 README файли для кожної директорії")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка при розгортанні шаблону: {e}")
        return False

def option_2_convert_drakon():
    """Варіант 2: Конвертувати DRAKON схеми"""
    print("\n" + "🔄"*20)
    print("--- ВАРІАНТ 2: Конвертація DRAKON схем ---")
    print("🔄"*20)
    
    drn_dir = Path("drn")
    if not drn_dir.exists():
        print("❌ ПОМИЛКА: Директорія drn/ не існує!")
        print("💡 Спочатку виберіть варіант 1 для розгортання шаблону.")
        return False
    
    json_files = list(drn_dir.glob("*.json"))
    
    if not json_files:
        print("🔭 У папці drn/ не знайдено .json файлів.")
        print("💡 Помістіть DRAKON схеми (.json) в папку drn/ та спробуйте знову.")
        return False
    
    print(f"📋 Знайдено {len(json_files)} файл(ів) для конвертації:")
    for json_file in json_files:
        print(f"   📄 {json_file.name}")
    
    converted_count = 0
    errors = []
    
    for json_file in json_files:
        try:
            print(f"\n📄 Конвертуємо: {json_file.name}")
            md_file = json_file.with_suffix('.md')
            
            result = subprocess.run([
                sys.executable, "drakon_converter.py", 
                str(json_file), "-o", str(md_file)
            ], capture_output=True, text=True)
            
            if md_file.exists():
                print(f"   ✓ {md_file.name}")
                size = md_file.stat().st_size
                print(f"   📏 Розмір: {size:,} байт")
                converted_count += 1
            else:
                errors.append(f"{json_file.name}: Не вдалося створити файл")
                print(f"   ❌ {json_file.name}: Помилка конвертації")
                
        except Exception as e:
            errors.append(f"{json_file.name}: {str(e)}")
            print(f"   ❌ {json_file.name}: {str(e)}")
    
    print(f"\n📊 Результат конвертації:")
    print(f"   ✅ Успішно: {converted_count}")
    print(f"   ❌ Помилки: {len(errors)}")
    
    return converted_count > 0

def option_3_create_md():
    """Варіант 3: Створити файл з коду проєкту"""
    print("\n" + "📄"*20)
    print("--- ВАРІАНТ 3: Створення узагальнюючого файлу ---")
    print("📄"*20)
    
    # Отримуємо цільову директорію
    target_dir = get_target_directory()
    if target_dir is None:
        return False
    
    project_name = target_dir.name
    
    # Вибір формату файлу
    print("\n📝 Виберіть формат вихідного файлу:")
    print("1. 📄 .md (Markdown)")
    print("2. 📃 .txt (Plain Text)")
    print("3. 📕 .pdf (PDF Document) - для NotebookLM")
    
    format_choice = input("👉 Введіть номер (1-3, Enter для .md): ").strip()
    
    if format_choice == "2":
        file_extension = ".txt"
        format_name = "Plain Text"
    elif format_choice == "3":
        try:
            from reportlab.lib.pagesizes import A4
            file_extension = ".pdf"
            format_name = "PDF Document"
        except ImportError:
            print("\n❌ Для створення PDF потрібні додаткові пакети!")
            print("💡 Запустіть скрипт спочатку для встановлення залежностей.")
            return False
    else:
        file_extension = ".md"
        format_name = "Markdown"
    
    # Результат зберігається в директорії скрипта
    output_file = SCRIPT_DIR / f"{project_name}{file_extension}"
    
    print(f"\n📁 Цільова директорія для обробки: {target_dir}")
    print(f"📋 Назва проєкту: {project_name}")
    print(f"📄 Вихідний файл: {output_file} ({format_name})")
    print(f"💾 Результат буде збережено: {SCRIPT_DIR}")
    print("\n⚠️ УВАГА:")
    print("   ✅ Приховані ФАЙЛИ (.env, .gitignore тощо) БУДУТЬ включені")
    print("   ❌ Приховані ДИРЕКТОРІЇ (.git, .venv тощо) НЕ будуть включені")
    print("   ❌ Сервісні файли будуть виключені")
    
    try:
        print(f"\n📄 Створюємо файл...")
        
        valid_extensions = {'.py', '.js', '.ts', '.html', '.css', '.md', '.txt', 
                           '.yml', '.yaml', '.json', '.xml', '.sql', '.sh', '.bat',
                           '.jsx', '.tsx', '.vue', '.svelte', '.php', '.java', '.cs',
                           '.cpp', '.c', '.h', '.hpp', '.rb', '.go', '.rs', '.swift',
                           '.env', '.gitignore', '.dockerignore', '.editorconfig'}
        
        processed_files = 0
        total_size = 0
        skipped_files = 0
        hidden_files_count = 0
        
        # Створюємо markdown контент
        md_content = []
        
        # Заголовок
        md_content.append(f"# Код проєкту: {project_name}\n\n")
        md_content.append(f"**Згенеровано:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        md_content.append(f"**Директорія:** `{target_dir}`\n")
        md_content.append(f"**Формат:** {format_name}\n\n")
        md_content.append("---\n\n")
        
        # Структура проєкту
        md_content.append("## Структура проєкту\n\n```\n")
        tree_structure = get_tree_structure(str(target_dir), SERVICE_DIRS)
        md_content.append(tree_structure)
        md_content.append("```\n\n---\n\n")
        
        # Файли
        md_content.append("## Файли проєкту\n\n")
        
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in SERVICE_DIRS and not d.startswith('.')]
            
            for file_name in files:
                if file_name in SERVICE_FILES:
                    skipped_files += 1
                    print(f"⏭️ Пропущено (сервісний): {file_name}")
                    continue
                
                is_hidden = file_name.startswith('.')
                _, extension = os.path.splitext(file_name)
                
                if not (extension.lower() in valid_extensions or is_hidden or extension == ''):
                    continue
                
                if file_name == output_file.name:
                    continue
                
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, target_dir)
                
                try:
                    file_size = os.path.getsize(full_path)
                    
                    md_content.append(f"### {relative_path}\n\n")
                    md_content.append(f"**Розмір:** {file_size:,} байт")
                    if is_hidden:
                        md_content.append(f" | 👁️ **Прихований файл**")
                    md_content.append("\n\n")
                    
                    lang_map = {
                        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                        '.html': 'html', '.css': 'css', '.yml': 'yaml', 
                        '.yaml': 'yaml', '.json': 'json', '.xml': 'xml',
                        '.sql': 'sql', '.sh': 'bash', '.bat': 'batch',
                        '.jsx': 'jsx', '.tsx': 'tsx', '.vue': 'vue',
                        '.php': 'php', '.java': 'java', '.cs': 'csharp',
                        '.cpp': 'cpp', '.c': 'c', '.rb': 'ruby',
                        '.go': 'go', '.rs': 'rust', '.swift': 'swift',
                        '.env': 'bash', '.gitignore': 'text'
                    }
                    lang = lang_map.get(extension.lower(), 'text')
                    md_content.append(f"```{lang}\n")
                    
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        md_content.append(content)
                        if not content.endswith('\n'):
                            md_content.append('\n')
                        processed_files += 1
                        total_size += file_size
                        
                        if is_hidden:
                            hidden_files_count += 1
                            print(f"👁️ Додано (прихований): {relative_path} ({file_size:,} байт)")
                        else:
                            print(f"✅ Додано: {relative_path} ({file_size:,} байт)")
                        
                except UnicodeDecodeError:
                    md_content.append("[Неможливо прочитати файл у форматі UTF-8]")
                    print(f"⚠️ ПОПЕРЕДЖЕННЯ: {relative_path} - помилка кодування")
                except Exception as e:
                    md_content.append(f"[Помилка: {str(e)}]")
                    print(f"❌ ПОМИЛКА: {relative_path} - {str(e)}")
                
                md_content.append("\n```\n\n")
        
        # Статистика
        md_content.append("---\n\n## Статистика\n\n")
        md_content.append(f"- **Оброблено файлів:** {processed_files}\n")
        md_content.append(f"- **З них прихованих файлів:** {hidden_files_count}\n")
        md_content.append(f"- **Пропущено сервісних файлів:** {skipped_files}\n")
        md_content.append(f"- **Загальний розмір:** {total_size:,} байт ({total_size/1024:.1f} KB)\n")
        md_content.append(f"- **Дата створення:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        full_md_content = ''.join(md_content)
        
        # Зберігаємо відповідно до формату
        if file_extension == ".pdf":
            print("\n📕 Конвертація в PDF...")
            success = convert_md_to_pdf(full_md_content, str(output_file), project_name)
            if not success:
                print("❌ Помилка конвертації в PDF")
                return False
        elif file_extension == ".txt":
            with open(output_file, 'w', encoding='utf-8') as f:
                plain_text = full_md_content.replace('**', '').replace('`', '')
                f.write(plain_text)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_md_content)
        
        print(f"\n✅ Файл {output_file.name} успішно створено!")
        print(f"📄 Вміст проєкту зібрано в один {format_name} файл.")
        print(f"💾 Збережено в: {output_file}")
        print(f"📊 Оброблено: {processed_files} файлів")
        print(f"👁️ З них прихованих: {hidden_files_count} файлів")
        print(f"⏭️ Пропущено сервісних: {skipped_files} файлів")
        print(f"📏 Загальний розмір вхідних файлів: {total_size:,} байт ({total_size/1024:.1f} KB)")
        
        if output_file.exists():
            size = output_file.stat().st_size
            print(f"📏 Розмір результату: {size:,} байт ({size/1024/1024:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_md_to_pdf(md_content, output_file, project_name):
    """Конвертує markdown контент в PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
        from reportlab.lib.enums import TA_LEFT, TA_CENTER
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8
        )
        
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Code'],
            fontSize=8,
            leftIndent=10,
            textColor=colors.HexColor('#2c3e50'),
            backColor=colors.HexColor('#f5f5f5')
        )
        
        story = []
        lines = md_content.split('\n')
        in_code_block = False
        code_buffer = []
        
        for line in lines:
            if line.startswith('```'):
                if in_code_block:
                    if code_buffer:
                        code_text = '\n'.join(code_buffer)
                        if len(code_text) > 10000:
                            code_text = code_text[:10000] + "\n... (код обрізано для PDF)"
                        try:
                            pre = Preformatted(code_text, code_style)
                            story.append(pre)
                        except:
                            p = Paragraph(code_text.replace('<', '&lt;').replace('>', '&gt;'), styles['Code'])
                            story.append(p)
                        story.append(Spacer(1, 0.3*cm))
                    code_buffer = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue
            
            if in_code_block:
                code_buffer.append(line)
                continue
            
            if line.startswith('# '):
                story.append(Paragraph(line[2:], title_style))
                story.append(Spacer(1, 0.5*cm))
            elif line.startswith('## '):
                story.append(Spacer(1, 0.3*cm))
                story.append(Paragraph(line[3:], heading_style))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], subheading_style))
            elif line.startswith('---'):
                story.append(Spacer(1, 0.5*cm))
            elif line.strip() and not line.startswith('**'):
                clean_line = line.replace('**', '').replace('`', '')
                if clean_line.strip():
                    try:
                        p = Paragraph(clean_line, styles['Normal'])
                        story.append(p)
                    except:
                        pass
        
        print("   📝 Генерація PDF документу...")
        doc.build(story)
        print("   ✅ PDF створено успішно!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Помилка при створенні PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_tree_structure(root_dir, ignore_dirs, prefix="", max_depth=3, current_depth=0):
    """Повертає структуру дерева як рядок"""
    result = []
    
    if current_depth >= max_depth:
        return ""
    
    try:
        items = sorted(os.listdir(root_dir))
        
        dirs = []
        files = []
        
        for item in items:
            item_path = os.path.join(root_dir, item)
            
            if os.path.isdir(item_path):
                if item not in ignore_dirs and not item.startswith('.'):
                    dirs.append(item)
            else:
                if item not in SERVICE_FILES:
                    files.append(item)
        
        for i, directory in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and not files
            result.append(f"{prefix}{'└── ' if is_last_dir else '├── '}{directory}/\n")
            
            extension = "    " if is_last_dir else "│   "
            subtree = get_tree_structure(
                os.path.join(root_dir, directory),
                ignore_dirs,
                prefix + extension,
                max_depth,
                current_depth + 1
            )
            result.append(subtree)
        
        display_files = files[:15]
        for i, file in enumerate(display_files):
            is_last = i == len(display_files) - 1
            hidden_mark = " [hidden]" if file.startswith('.') else ""
            result.append(f"{prefix}{'└── ' if is_last else '├── '}{file}{hidden_mark}\n")
        
        if len(files) > 15:
            result.append(f"{prefix}└── ... та ще {len(files) - 15} файлів\n")
            
    except PermissionError:
        result.append(f"{prefix}└── [Немає доступу]\n")
    
    return ''.join(result)

def option_4_copy_md():
    """Варіант 4: Копіювати файл до Dropbox або іншої директорії"""
    print("\n" + "📤"*20)
    print("--- ВАРІАНТ 4: Копіювання файлу ---")
    print("📤"*20)
    
    # Шукаємо файли в директорії скрипта
    md_files = list(SCRIPT_DIR.glob("*.md"))
    txt_files = list(SCRIPT_DIR.glob("*.txt"))
    pdf_files = list(SCRIPT_DIR.glob("*.pdf"))
    all_files = md_files + txt_files + pdf_files
    
    if not all_files:
        print(f"❌ У директорії {SCRIPT_DIR} не знайдено .md, .txt або .pdf файлів")
        print("💡 Спочатку створіть файл (варіант 3)")
        return False
    
    print("📋 Знайдені файли:")
    for i, file in enumerate(all_files, 1):
        size = file.stat().st_size
        file_type_map = {".md": "Markdown", ".txt": "Text", ".pdf": "PDF"}
        file_type = file_type_map.get(file.suffix, "Unknown")
        size_mb = size / 1024 / 1024
        if size_mb > 1:
            size_str = f"{size_mb:.2f} MB"
        else:
            size_str = f"{size:,} байт"
        print(f"   {i}. {file.name} ({size_str}) [{file_type}]")
    
    if len(all_files) == 1:
        selected_file = all_files[0]
        print(f"\n📄 Автоматично вибрано: {selected_file.name}")
    else:
        try:
            choice = input(f"\n🔢 Виберіть файл для копіювання (1-{len(all_files)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(all_files):
                selected_file = all_files[idx]
            else:
                print("❌ Невірний вибір")
                return False
        except ValueError:
            print("❌ Введіть число")
            return False
    
    default_dir = Path(r"C:\Users\tukro\Dropbox\Приложения\remotely-save\olena")
    
    print(f"\n📁 Директорія за замовчуванням:")
    print(f"   {default_dir}")
    
    custom_path = input("\n📂 Введіть шлях для копіювання (Enter для використання за замовчуванням): ").strip()
    
    if custom_path:
        custom_path = os.path.expanduser(custom_path)
        target_dir = Path(custom_path)
    else:
        target_dir = default_dir
    
    if not target_dir.exists():
        print(f"⚠️ Директорія не існує: {target_dir}")
        create = input("❓ Створити директорію? (y/n): ").strip().lower()
        if create == 'y':
            try:
                target_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ Директорію створено: {target_dir}")
            except Exception as e:
                print(f"❌ Не вдалося створити директорію: {e}")
                return False
        else:
            print("❌ Копіювання скасовано")
            return False
    
    target_file = target_dir / selected_file.name
    
    try:
        if target_file.exists():
            print(f"⚠️ Файл вже існує: {target_file}")
            overwrite = input("❓ Перезаписати? (y/n): ").strip().lower()
            if overwrite != 'y':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target_file = target_dir / f"{selected_file.stem}_{timestamp}{selected_file.suffix}"
                print(f"📝 Новий файл: {target_file.name}")
        
        shutil.copy2(selected_file, target_file)
        
        print(f"\n✅ Файл успішно скопійовано!")
        print(f"📤 Джерело: {selected_file}")
        print(f"📥 Призначення: {target_file}")
        
        if target_file.exists():
            size = target_file.stat().st_size
            size_mb = size / 1024 / 1024
            if size_mb > 1:
                print(f"📏 Розмір: {size_mb:.2f} MB")
            else:
                print(f"📏 Розмір: {size:,} байт")
        
        if selected_file.suffix == ".pdf":
            print("\n💡 Тепер ви можете завантажити цей PDF в NotebookLM!")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка копіювання: {e}")
        return False

def create_codetomd_file():
    """Створює файл codetomd.py"""
    content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code to Markdown Converter - Helper Script
"""

import os
import sys
from pathlib import Path
from datetime import datetime

SERVICE_FILES = {
    'codetomd.py', 'codetomd.bat', 'drakon_converter.py',
    'md_to_embeddings_service.py', 'md_to_embeddings_service_v4.py',
    'md-to-embeddings-service.bat', 'run_md_service.sh'
}

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    project_name = Path(root_dir).resolve().name
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"{project_name}.md"
    
    extensions = {'.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.json', '.yml', '.yaml'}
    ignore_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.vscode', '.idea'}
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"# {project_name}\\n\\n")
        out.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        
        count = 0
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
            for file in files:
                if file in SERVICE_FILES:
                    continue
                if Path(file).suffix in extensions or file.startswith('.'):
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, root_dir)
                    out.write(f"## {relpath}\\n\\n```\\n")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            out.write(f.read())
                            out.write("\\n```\\n\\n")
                            count += 1
                            print(f"Added: {relpath}")
                    except:
                        out.write("[Could not read file]\\n```\\n\\n")
        
        print(f"Processed {count} files")

if __name__ == "__main__":
    main()
'''
    
    with open("codetomd.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_drakon_converter_file():
    """Створює файл drakon_converter.py"""
    content = '''#!/usr/bin/env python3
"""
DRAKON to Markdown Converter
"""

import json
import sys
from datetime import datetime

def convert_drakon_to_markdown(input_file, output_file=None):
    if not output_file:
        output_file = input_file.replace('.json', '.md')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# DRAKON Схема\\n\\n")
            f.write(f"**Джерело:** `{input_file}`\\n")
            f.write(f"**Конвертовано:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            
            nodes = data.get('nodes', {})
            f.write("## Вузли\\n\\n")
            for node_id, node_data in nodes.items():
                node_type = node_data.get('type', 'unknown')
                content = node_data.get('content', {})
                text = content.get('txt', '') if isinstance(content, dict) else str(content)
                f.write(f"- **{node_id}** ({node_type}): {text}\\n")
        
        print(f"Конвертовано: {output_file}")
        return True
        
    except Exception as e:
        print(f"Помилка: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Використання: python drakon_converter.py input.json [-o output.md]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "-o" else None
    convert_drakon_to_markdown(input_file, output_file)

if __name__ == "__main__":
    main()
'''
    
    with open("drakon_converter.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_readme_files():
    """Створює README файли для директорій"""
    
    readme_content = {
        "code": """# 📁 Code Directory

Директорія для збереження вихідного коду проєктів.

## Призначення
- Тимчасове збереження коду для аналізу
- Архівування версій коду
- Підготовка файлів для конвертації в markdown

## Використання
Помістіть сюди ваші проєкти для подальшого перетворення в markdown файли.
""",
        "drn": """# 📁 DRN Directory (DRAKON Files)

Директорія для DRAKON схем у форматі JSON.

## Призначення
- Збереження DRAKON схем (.json файли)
- Вхідні дані для конвертації в markdown

## Використання
1. Помістіть .json файли зі схемами в цю директорію
2. Запустіть варіант 2 в головному меню для конвертації
""",
        "srv": """# 📁 SRV Directory (Services)

Директорія для сервісних файлів та конфігурацій.

## Призначення
- Конфігураційні файли
- Допоміжні скрипти
- Логи та тимчасові файли
"""
    }
    
    for dirname, content in readme_content.items():
        readme_path = Path(dirname) / "README.md"
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✓ {readme_path}")
        except Exception as e:
            print(f"   ❌ Помилка створення {readme_path}: {e}")

def main():
    """Головна функція програми"""
    print("🚀 Запуск MD to Embeddings Service v4.3")
    print("📅 Дата:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"📁 Директорія скрипта: {SCRIPT_DIR}")
    print(f"📁 Робоча директорія: {Path.cwd()}")
    
    # Перевірка залежностей при запуску
    deps_ok = check_dependencies()
    
    while True:
        try:
            show_menu()
            choice = input("\n👉 Введіть номер варіанту (1-5): ").strip()
            
            if choice == "1":
                success = option_1_deploy_template()
                if success:
                    input("\n✅ Натисніть Enter для продовження...")
                else:
                    input("\n❌ Натисніть Enter для продовження...")
            
            elif choice == "2":
                success = option_2_convert_drakon()
                if success:
                    input("\n✅ Натисніть Enter для продовження...")
                else:
                    input("\n❌ Натисніть Enter для продовження...")
            
            elif choice == "3":
                success = option_3_create_md()
                if success:
                    input("\n✅ Натисніть Enter для продовження...")
                else:
                    input("\n❌ Натисніть Enter для продовження...")
            
            elif choice == "4":
                success = option_4_copy_md()
                if success:
                    input("\n✅ Натисніть Enter для продовження...")
                else:
                    input("\n❌ Натисніть Enter для продовження...")
            
            elif choice == "5":
                print("\n👋 До побачення!")
                print("📊 Дякуємо за використання MD to Embeddings Service!")
                break
            
            else:
                print("\n❌ Неправильний вибір! Виберіть число від 1 до 5.")
                input("Натисніть Enter для продовження...")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Програму перервано користувачем.")
            print("👋 До побачення!")
            break
        except Exception as e:
            print(f"\n❌ Неочікувана помилка: {e}")
            input("Натисніть Enter для продовження...")

if __name__ == "__main__":
    main()