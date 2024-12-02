import tkinter as tk
from tkinter import messagebox
import os

# 즐겨찾기 파일 경로
favorites_file = "like.txt"

# 메모리 내 즐겨찾기 데이터 구조
favorite_words = []

# 'like.txt' 파일에서 단어 읽기
def load_favorites_from_file():
    if os.path.exists(favorites_file):
        try:
            with open(favorites_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():  # 비어 있는 줄은 무시
                        # 단어와 번역 정보 분리
                        word_data = line.split(":")
                        if len(word_data) == 2:  # 형식이 올바른 경우
                            word = word_data[0].strip()  # 단어 추출
                            translations = word_data[1].strip()  # 번역 정보 추출

                            # 번역 정보를 , 로 나누고 각 언어별로 분리
                            translation_parts = translations.split(",")
                            english = ""
                            french = ""
                            german = ""

                            for part in translation_parts:
                                part = part.strip()
                                if part.startswith("English="):
                                    english = part.split("=")[1].strip()
                                elif part.startswith("German="):
                                    german = part.split("=")[1].strip()
                                elif part.startswith("French="):
                                    french = part.split("=")[1].strip()

                            # 단어를 즐겨찾기 리스트에 추가
                            favorite_words.append({"word": word, "English": english, "French": french, "German": german})
                        else:
                            messagebox.showwarning("파일 형식 오류", f"잘못된 형식의 데이터가 발견되었습니다: {line}")
        except UnicodeDecodeError:
            messagebox.showerror("파일 읽기 오류", "파일을 UTF-8로 읽는 도중 오류가 발생했습니다.")
    else:
        messagebox.showinfo("파일 없음", f"'{favorites_file}' 파일이 존재하지 않습니다.")

# 검색된 단어 화면 업데이트
def update_searched_words_display(frame):
    """단어 목록을 업데이트하고 화면에 표시"""
    for widget in frame.winfo_children():
        widget.destroy()  # 기존의 모든 위젯을 삭제

    if favorite_words:
        for word_data in favorite_words:
            word_row = tk.Frame(frame, bg="white", relief="solid")
            word_row.pack(fill="x", pady=2)

            # 단어들 간의 간격을 좁히기 위해 padx 값을 줄였습니다.
            tk.Label(word_row, text=word_data["word"], bg="white", font=("Arial", 10), width=10, anchor="w").pack(side="left", padx=2)
            tk.Label(word_row, text=word_data["English"], bg="white", font=("Arial", 10), width=10, anchor="w").pack(side="left", padx=2)
            tk.Label(word_row, text=word_data["French"], bg="white", font=("Arial", 10), width=10, anchor="w").pack(side="left", padx=2)
            tk.Label(word_row, text=word_data["German"], bg="white", font=("Arial", 10), width=10, anchor="w").pack(side="left", padx=2)
    else:
        tk.Label(frame, text="즐겨찾기된 단어가 없습니다.", bg="white", font=("Arial", 12)).pack(pady=20)

# 단어 모음집 GUI 화면
def display_word_collection():
    """단어 모음집 화면"""
    def close_window():
        """창 닫기 함수 (알림 없이 바로 종료)"""
        window.destroy() 

    # GUI 생성
    window = tk.Tk()  # 새 창 생성
    window.title("단어 모음집")
    window.geometry("400x400")
    window.config(bg="lightblue")

    # 상단 종료 버튼
    close_button = tk.Button(window, text="종료", command=close_window, bg="red", fg="white", font=("Arial", 10))
    close_button.pack(anchor="nw", padx=10, pady=10)

    # 제목 라벨
    title_label = tk.Label(window, text="단어 모음집", bg="lightblue", font=("Arial", 16, "bold"))
    title_label.pack(pady=5)

    # 데이터 표시 프레임
    frame = tk.Frame(window, bg="white", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    # 데이터 표시 (헤더)
    header = tk.Frame(frame, bg="lightgray", relief="solid")
    header.pack(fill="x")

    tk.Label(header, text="단어", bg="lightgray", font=("Arial", 12), width=10, anchor="w").pack(side="left", padx=2)
    tk.Label(header, text="영어", bg="lightgray", font=("Arial", 12), width=10, anchor="w").pack(side="left", padx=2)
    tk.Label(header, text="프랑스어", bg="lightgray", font=("Arial", 12), width=10, anchor="w").pack(side="left", padx=2)
    tk.Label(header, text="독일어", bg="lightgray", font=("Arial", 12), width=10, anchor="w").pack(side="left", padx=2)

    # 단어 목록 표시
    update_searched_words_display(frame)

    window.mainloop()

# 프로그램 독립 실행 시
if __name__ == "__main__":
    load_favorites_from_file()  # 파일에서 즐겨찾기 단어 불러오기 먼저 실행
    display_word_collection()   # 단어 모음집 화면 띄우기