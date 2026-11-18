
from router import blue_green_router, canary_router

print("BLUE-GREEN DEPLOYMENT")

print("Before switching:")
print(blue_green_router("blue"))

print("\nAfter switching:")
print(blue_green_router("green"))


print("\nCANARY DEPLOYMENT")

new_version_count = 0

for request in range(1, 21):
    response = canary_router(request)

    if "v2" in response:
        new_version_count += 1

    print(f"Request {request}: {response}")

percentage = (new_version_count / 20) * 100

print(f"\nNew version traffic: {percentage}%")
