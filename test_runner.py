import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ส่วนตั้งค่าโจทย์และ Test Cases (ข้อละ 4 Test Cases = ข้อละ 4 คะแนน)
# รูปแบบ: "ชื่อไฟล์": [
#     ([ข้อมูล Input บรรทัดที่ 1, บรรทัดที่ 2], "ผลลัพธ์ Output ที่ถูกต้อง"),
# ]
# ==============================================================================
EXAM_TEST_CASES = {
    "Examination_1": [
        (["10", "5"], "25.0"),     # Test Case 1 (1 คะแนน)
        (["3.5", "2.0"], "3.5"),    # Test Case 2 (1 คะแนน)
        (["0", "5"], "0.0"),       # Test Case 3 (1 คะแนน)
        (["100", "200"], "10000.0") # Test Case 4 (1 คะแนน)
    ],
    "Examination_2": [
        (["10", "5"], "50.0"),
        (["3.5", "2.0"], "7.0"),
        (["0", "5"], "0.0"),
        (["10", "10"], "100.0")
    ],
    "Examination_3": [
        (["80"], "A"),
        (["70"], "B"),
        (["60"], "C"),
        (["49"], "F")
    ],
    "Examination_4": [
        (["5"], "15"),
        (["1"], "1"),
        (["10"], "55"),
        (["0"], "0")
    ],
    "Examination_5": [
        (["2"], "Even"),
        (["3"], "Odd"),
        (["0"], "Even"),
        (["-1"], "Odd")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์ว่ามีนามสกุล .py หรือไม่เพื่อป้องกันข้อผิดพลาดการตั้งชื่อ"""
    if os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name):
        return base_name
    return None

def run_test(file_path, inputs):
    """รันไฟล์ Python พร้อมส่ง Input และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if output is not None and output.strip() == expected.strip():
                    passed_cases += 1
        
        # คำนวณคะแนนยืดหยุ่น (1 เคสผ่าน = 1 คะแนน)
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        # ไอคอนสถานะ
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    # สร้าง Markdown Summary แสดงในหน้า GitHub Actions Summary
    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    # ส่งผลคะแนนเข้า $GITHUB_STEP_SUMMARY ของ GitHub Actions
    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
