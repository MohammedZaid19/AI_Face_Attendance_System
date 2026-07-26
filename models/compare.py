print("=" * 80)
print("             AI FACE ATTENDANCE SYSTEM")
print("        Face Detection Model Benchmark")
print("=" * 80)

print()

print("{:<18} {:<18} {:<20} {:<10}".format(
    "Model",
    "Faces Detected",
    "Avg Time (sec)",
    "FPS"
))

print("-" * 80)

models = [
    {
        "name": "Haar Cascade",
        "faces": 773,
        "time": 0.1210,
        "fps": 8.27
    },
    {
        "name": "YuNet",
        "faces": 1100,
        "time": 0.0949,
        "fps": 10.53
    },
    {
        "name": "YOLO11n",
        "faces": "Person Detection",
        "time": 0.2470,
        "fps": 4.05
    }
]

for model in models:

    print("{:<18} {:<18} {:<20} {:<10}".format(
        model["name"],
        str(model["faces"]),
        model["time"],
        model["fps"]
    ))

print("-" * 80)

print("\nPerformance Ranking")
print("----------------------------")
print("🥇 1. YuNet")
print("🥈 2. Haar Cascade")
print("🥉 3. YOLO11n")

print("\nRecommendation")
print("----------------------------")
print("Winner : YuNet")

print("""
Reason:

✓ Highest FPS (10.53)

✓ Lowest Detection Time (0.0949 sec)

✓ Highest Number of Faces Detected (1100)

✓ Lightweight Face Detector

✓ CPU Friendly

✓ Designed Specifically for Face Detection

✓ Suitable for Real-Time Attendance System
""")

print("=" * 80)