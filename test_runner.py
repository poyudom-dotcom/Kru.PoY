import os
import subprocess

# 1. ปรับชุดข้อมูลทดสอบ
TEST_CASES = {
    "Examination_1": [
        # Test cases เดิมของครูข้อ 1
    ],
    "Examination_2": [
        # Test cases เดิมของครูข้อ 2
    ],
    "Examination_3": [
        # Test cases เดิมของครูข้อ 3
    ],
    "Examination_4": [
        # Test cases เดิมของครูข้อ 4
    ],
    "Examination_5": [
        {"input": "3\n", "expected": "60"},
        {"input": "5\n", "expected": "90"},
        {"input": "10\n", "expected": "190"}
    ]
}

def run_tests():
    all_passed = True
    
    for file_name, cases in TEST_CASES.items():
        py_file = f"{file_name}.py"
        if not os.path.exists(py_file):
            continue

        print(f"\n--- Testing {py_file} ---")
        for i, case in enumerate(cases, 1):
            process = subprocess.Popen(
                ["python", py_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=case["input"])
            
            # 2. ปรับการเปรียบเทียบให้ยืดหยุ่น
            actual_output = stdout.strip().lower()
            expected_output = case["expected"].strip().lower()
            
            if actual_output == expected_output:
                print(f"  Test Case {i}: PASSED ✅")
            else:
                print(f"  Test Case {i}: FAILED ❌ (Got: '{stdout.strip()}', Expected: '{case['expected']}')")
                all_passed = False

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    run_tests()
