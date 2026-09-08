import subprocess
import sys

# กำหนด Test Cases ของไฟล์ Examination_1 ถึง 5
TESTS = {
    "Examination_1": [
        {"input": "Somchai\n", "expected": "Hello, Somchai"}
    ],
    "Examination_2": [
        {"input": "100\n20\n", "expected": "80.0"}
    ],
    "Examination_3": [
        {"input": "75\n", "expected": "Pass"},
        {"input": "40\n", "expected": "Fail"}
    ],
    "Examination_4": [
        {"input": "85\n", "expected": "A"},
        {"input": "65\n", "expected": "B"}
    ],
    "Examination_5": [
        {"input": "3\n", "expected": "100"}
    ]
}

has_failed = False

for filename, test_cases in TESTS.items():
    for case in test_cases:
        try:
            res = subprocess.run(
                ["python", filename],
                input=case["input"],
                text=True,
                capture_output=True,
                timeout=3
            )
            output = res.stdout.strip()
            if case["expected"] not in output:
                print(f"❌ {filename} ไม่ผ่าน: ได้รับ '{output}' (คาดหวัง '{case['expected']}')")
                has_failed = True
            else:
                print(f"✅ {filename} ผ่าน!")
        except Exception as e:
            print(f"❌ {filename} เกิดข้อผิดพลาด: {e}")
            has_failed = True

if has_failed:
    sys.exit(1)  # แจ้ง GitHub Actions ว่าไม่ผ่าน (แสดงเครื่องหมาย ❌)
