import tkinter as tk
from tkinter import simpledialog, messagebox
import os

# 단어 저장 리스트
searched_words = {"Korean": [], "English": [], "French": [], "German": []}

# 단어 저장 및 검색 기록 파일 경로
history_file = "words.txt"
like_file = "like.txt"

# 'words.txt' 파일에서 단어 읽기
def load_words_from_file():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8", errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        # 각 언어를 분리하여 단어 리스트에 추가
                        parts = line.split("   ")  # 각 언어는 공백 3개로 구분되어 있다고 가정
                        if len(parts) == 4:
                            korean_part = parts[0].split(":")[1].strip()
                            english_part = parts[1].split(":")[1].strip()
                            french_part = parts[2].split(":")[1].strip()
                            german_part = parts[3].split(":")[1].strip()
                            searched_words["English"].append(english_part)
                            searched_words["French"].append(french_part)
                            searched_words["German"].append(german_part)
                            searched_words["Korean"].append(korean_part)
                        else:
                            # 잘못된 형식의 라인 건너뛰기
                            print(f"잘못된 형식의 라인 발견: {line}")
        except UnicodeDecodeError:
            with open(history_file, "r", encoding="ISO-8859-1") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        parts = line.split("   ")
                        if len(parts) == 4:
                            korean_part = parts[0].split(":")[1].strip()
                            english_part = parts[1].split(":")[1].strip()
                            french_part = parts[2].split(":")[1].strip()
                            german_part = parts[3].split(":")[1].strip()
                            searched_words["English"].append(english_part)
                            searched_words["French"].append(french_part)
                            searched_words["German"].append(german_part)
                            searched_words["Korean"].append(korean_part)

# 단어 검색 및 뜻을 출력하는 함수
def search_word():
    word = simpledialog.askstring("Input", "검색할 단어를 입력하세요:")
    if word:
        word = word.strip().lower()  # 입력값 공백 제거 및 소문자로 변환
        found = False
        translations = {"English": "", "French": "", "German": "", "Korean": ""}
        
        for lang, words in searched_words.items():
            if word in words:
                found = True
                idx = words.index(word)
                translations["English"] = searched_words["English"][idx]
                translations["French"] = searched_words["French"][idx]
                translations["German"] = searched_words["German"][idx]
                translations["Korean"] = searched_words["Korean"][idx]

        if found:
            update_searched_words_display()
            messagebox.showinfo("단어 뜻", f"'{word}'의 번역:\n"
                                          f"Korean: {translations['Korean']}\n"
                                          f"English: {translations['English']}\n"
                                          f"French: {translations['French']}\n"
                                          f"German: {translations['German']}")
        else:
            messagebox.showinfo("단어 뜻", f"'{word}'에 대한 뜻을 찾을 수 없습니다.")
    else:
        messagebox.showwarning("경고", "단어를 입력하지 않았습니다.")


# 즐겨찾기 저장
def add_to_favorites(english_word, french_word, german_word, korean_word):
    with open(like_file, "a", encoding="utf-8") as file:
        file.write(f"한국어: {korean_word} 영어: {english_word} 프랑스어: {french_word} 독일어: {german_word}\n")
    messagebox.showinfo("즐겨찾기", f"'{korean_word}', '{english_word}', '{french_word}', '{german_word}'을(를) 즐겨찾기에 추가했습니다.")

# 단어 삭제 (세 언어에서 동시에 삭제)
def delete_word(english_word, french_word, german_word, korean_word):
    with open(history_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(history_file, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip():
                if korean_word not in line and english_word not in line and french_word not in line and german_word not in line:
                    file.write(line)
    
    if english_word in searched_words["English"]:
        searched_words["English"].remove(english_word)
    if french_word in searched_words["French"]:
        searched_words["French"].remove(french_word)
    if german_word in searched_words["German"]:
        searched_words["German"].remove(german_word)
    if korean_word in searched_words["Korean"]:
        searched_words["Korean"].remove(korean_word)

    update_searched_words_display()
    messagebox.showinfo("삭제", "삭제되었습니다.")

# 메인 창에 검색 기록 표시
def update_searched_words_display():

    for widget in history_frame.winfo_children():
        widget.destroy()

    # 폰트 설정
    header_font = ("Arial", 12, "bold")
    content_font = ("Arial", 10)
    button_font = ("Arial", 8)

    # 버튼 크기 설정
    button_width = 8
    
    # 전체 컨테이너 프레임
    container_frame = tk.Frame(history_frame)
    container_frame.pack(fill=tk.BOTH, expand=True, padx=5)

    # 각 언어별 프레임 생성
    korean_frame = tk.Frame(container_frame)
    english_frame = tk.Frame(container_frame)
    french_frame = tk.Frame(container_frame)
    german_frame = tk.Frame(container_frame)
    button_frame = tk.Frame(container_frame)


    korean_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    english_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    french_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    german_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    button_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    # 헤더 라벨과 단어들을 포함할 프레임
    kor_content = tk.Frame(korean_frame)
    eng_content = tk.Frame(english_frame)
    fr_content = tk.Frame(french_frame)
    ger_content = tk.Frame(german_frame)

    kor_content.pack(anchor='w', padx=10)
    eng_content.pack(anchor='w', padx=10)
    fr_content.pack(anchor='w', padx=10)
    ger_content.pack(anchor='w', padx=10)

    # 헤더 라벨
    tk.Label(kor_content, text="한국어", font=header_font).pack(anchor='w')
    tk.Label(eng_content, text="영어", font=header_font).pack(anchor='w')
    tk.Label(fr_content, text="프랑스어", font=header_font).pack(anchor='w')
    tk.Label(ger_content, text="독일어", font=header_font).pack(anchor='w')
    
    # 관리 헤더를 위한 별도의 프레임
    manage_header_frame = tk.Frame(button_frame, width=200)  # 버튼들의 총 너비에 맞춤
    manage_header_frame.pack(fill=tk.X, padx=10)
    tk.Label(manage_header_frame, text="관리", font=header_font).pack(expand=True)

    max_words = max(len(searched_words["English"]), len(searched_words["French"]), 
                   len(searched_words["German"]), len(searched_words["Korean"]))

    # 단어 컨테이너 생성
    kor_words = tk.Frame(kor_content)
    eng_words = tk.Frame(eng_content)
    fr_words = tk.Frame(fr_content)
    ger_words = tk.Frame(ger_content)
    
    kor_words.pack(anchor='w')
    eng_words.pack(anchor='w')
    fr_words.pack(anchor='w')
    ger_words.pack(anchor='w')
    

    for i in range(max_words):
        korean_word = searched_words["Korean"][i] if i < len(searched_words["Korean"]) else ""
        english_word = searched_words["English"][i] if i < len(searched_words["English"]) else ""
        french_word = searched_words["French"][i] if i < len(searched_words["French"]) else ""
        german_word = searched_words["German"][i] if i < len(searched_words["German"]) else ""
        
        # 각 단어를 해당 언어 프레임에 추가
        tk.Label(kor_words, text=korean_word, font=content_font).pack(anchor='w', pady=2)
        tk.Label(eng_words, text=english_word, font=content_font).pack(anchor='w', pady=2)
        tk.Label(fr_words, text=french_word, font=content_font).pack(anchor='w', pady=2)
        tk.Label(ger_words, text=german_word, font=content_font).pack(anchor='w', pady=2)
        
        # 버튼 프레임
        btn_container = tk.Frame(button_frame)
        btn_container.pack(fill=tk.X, padx=10)
        
        # 버튼들을 담을 내부 프레임 (가운데 정렬을 위해)
        inner_btn_frame = tk.Frame(btn_container)
        inner_btn_frame.pack(expand=True, pady=1)
        
        tk.Button(inner_btn_frame, text="즐겨찾기", 
                 command=lambda eng=english_word, fr=french_word, 
                                ger=german_word, kor=korean_word: 
                                add_to_favorites(eng, fr, ger, kor),
                 font=button_font,
                 width=button_width).pack(side=tk.LEFT, padx=2)
        
        tk.Button(inner_btn_frame, text="삭제", 
                 command=lambda eng=english_word, fr=french_word, 
                                ger=german_word, kor=korean_word: 
                                delete_word(eng, fr, ger, kor),
                 font=button_font,
                 width=button_width).pack(side=tk.LEFT, padx=2)
    
    
# GUI 인터페이스 만들기
root = tk.Tk()
root.title("단어 검색 프로그램")
root.geometry("500x400")

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

search_button = tk.Button(top_frame, text="단어 검색", command=search_word)
search_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(top_frame, text="종료", command=root.destroy)
exit_button.pack(side=tk.LEFT, padx=5)

history_frame = tk.Frame(root)
history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

load_words_from_file()
update_searched_words_display()

root.mainloop()
