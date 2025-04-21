import V8.v8_testing as v8Testing
import Firefox.firefox_testing as firefoxTesting
import Chrome.chrome_testing as chromeTesting


def run_all_tests():
    print("\nTesting V8:\n")
    v8_result = v8Testing.testV8()
    print("\nTesting Firefox:\n")
    firefox_result = firefoxTesting.testFirefox()
    print("\nTesting Chrome:\n")
    chrome_result = chromeTesting.testChrome()
    print()
    return v8_result == True and firefox_result == True and chrome_result == True

if __name__ == "__main__":
    result = run_all_tests()
    print(f"Are all tests successful?\n\t{result}\n")
