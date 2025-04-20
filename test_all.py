import V8.V8_testing as v8Testing
import Firefox.firefox_testing as firefoxTesting
import Chrome.chrome_testing as chromeTesting

print("\nTesting V8:\n")
v8Testing.testV8()

print("\nTesting Firefox:\n")
firefoxTesting.testFirefox()

print("\nTesting Chrome:\n")
chromeTesting.testChrome()

print()