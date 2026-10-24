# DA3 Video Demonstration: macOS Recording Guide
## Course: Cloud Architecture Design (BCSE355L) — Academic Year 2026–27
**Platform**: Apple macOS (Compatible with macOS Sonoma, Sequoia, Ventura, and Monterey)  
**Target Video Specs**: 1080p Full HD (1920 × 1080), 30 fps, AAC Stereo Audio, MP4 Format  
**Required Video Length**: Exactly 5 Minutes (05:00 ± 5 seconds)  

---

## 1. Why Native Recording by the Student is Required

> [!IMPORTANT]
> **Faculty Evaluation & Turnitin / Viva Compliance**:  
> University evaluation guidelines for BCSE355L mandate an **authentic student presentation**. The grading rubric assesses your vocal explanation, technical vocabulary, and live demonstration of the cloud infrastructure.  
> While automated tools and background scripts can generate headless screen captures, they **cannot capture your live speaking voice or personal viva defense**. Therefore, this guide details the exact steps to capture your screen and voice in flawless high definition on your Mac.

---

## 2. Method 1: Built-in macOS Screenshot Toolbar (`Command + Shift + 5`)

This is the cleanest, zero-install, native method built directly into macOS.

### Step 1: Open the Recording Bar
1. On your Mac keyboard, press:
   ```
   Command (⌘) + Shift (⇧) + 5
   ```
2. A floating toolbar appears at the bottom of the screen.

### Step 2: Configure Screen Capture Mode
1. In the toolbar, locate the two recording buttons in the middle:
   - **Record Entire Screen** (camera icon with a solid frame).
   - **Record Selected Portion** (camera icon with a dashed frame).
2. **Recommendation**: Click **Record Selected Portion** and drag the box to encompass your browser window at 1920×1080, OR click **Record Entire Screen** if your display is set to 1080p.

### Step 3: Configure Audio & Microphone
1. In the floating toolbar, click **Options**.
2. Under **Microphone**, select your microphone:
   - Select **Built-in Microphone** (or your connected USB headset/AirPods).
   - **CRITICAL**: Do NOT leave it on *"None"*, or the video will have no sound!
3. Under **Timer**, select **5 seconds**. This gives you 5 seconds to position your mouse on Tab 1 before recording starts.
4. Under **Save to**, choose **Desktop** or **Documents**.
5. Ensure **Show Mouse Clicks** is checked (this draws a subtle circle when you click, making your navigation easy for the faculty to follow).

### Step 4: Record
1. Click the **Record** button on the right side of the floating toolbar.
2. The 5-second countdown will tick down. Take a deep breath.
3. When the countdown completes, begin speaking Scene 1 from [`FINAL_5_MINUTE_SCRIPT.md`](file:///Users/nikhilanand/Downloads/Delta/docs/da3/demo-video/FINAL_5_MINUTE_SCRIPT.md).

### Step 5: Stop the Recording
1. When you conclude at the 5-minute mark, click the small circular **Stop Record** icon located in the **macOS top menu bar** (next to the WiFi and Battery icons):
   ```
   [ ● ]  <- Click this icon in the macOS menu bar to stop
   ```
   *Alternative shortcut*: Press `Command (⌘) + Control + Escape`.
2. A thumbnail preview appears in the bottom right corner of your screen. Wait 3 seconds for it to save to your chosen folder.

---

## 3. Method 2: QuickTime Player Recording

If you prefer using QuickTime Player:

1. Press `Command + Space`, type `QuickTime Player`, and press `Enter`.
2. In the top menu bar, click **File** -> **New Screen Recording**.
3. The same `Command + Shift + 5` recording bar opens. Follow Steps 2 through 5 above.
4. If an older QuickTime interface appears:
   - Click the small arrow next to the red Record button.
   - Select your **Microphone** and raise the volume slider slightly to hear input feedback.
   - Click the red Record button, click anywhere on screen to record full screen, and speak.

---

## 4. Perfect 5-Minute Trimming in QuickTime Player

If your video recorded for 5 minutes and 8 seconds, you can trim the exact start and end to hit 05:00.00 without re-encoding:

1. Double-click the saved `.mov` file to open it in **QuickTime Player**.
2. Press `Command (⌘) + T` (or click **Edit** -> **Trim**).
3. A yellow trimming bar appears at the bottom with start and end handles:
   - Drag the left yellow handle to the exact second where your speech begins (`00:00`).
   - Drag the right yellow handle to exactly `05:00`.
4. Click the yellow **Trim** button on the right.
5. Press `Command + S` to save the trimmed file.

---

## 5. Converting .MOV to Course-Compliant MP4 Using FFmpeg

macOS native screen recordings are saved as `.mov` (QuickTime container). Most academic portals (Moodle, Blackboard, Google Drive) prefer standard `.mp4` (H.264 video + AAC audio).

Because `ffmpeg` is already installed on your Mac, you can convert and compress your video in 5 seconds via your terminal:

```bash
# Convert and optimize for web/portal submission:
/opt/homebrew/bin/ffmpeg -i ~/Desktop/Screen\ Recording*.mov \
  -vcodec libx264 -crf 22 -preset medium \
  -acodec aac -b:a 192k \
  -movflags +faststart \
  docs/da3/demo-video/DA3_Algorithmic_Trading_AWS_Demo.mp4
```

### Why this command is optimal:
- `-crf 22`: Delivers visually lossless 1080p clarity while keeping the file size small (~35–50 MB for 5 minutes).
- `-movflags +faststart`: Places the MP4 metadata index at the beginning of the file, allowing instant streaming in browser evaluation players without buffering delays.
- `-b:a 192k`: High-fidelity stereo audio for clear voice presentation.

---

## 6. Pre-Submission Quality Checklist

Before submitting your MP4 video to your professor or portal:

| Verification Item | Requirement | Passed? |
| :--- | :--- | :---: |
| **Duration** | Between 04:55 and 05:05 (Target: exactly 05:00) | [ ] |
| **Audio Clarity** | Speech is loud, clear, and free from clipping or heavy echo | [ ] |
| **Video Resolution** | 1920 × 1080 (1080p Full HD) | [ ] |
| **Framerate** | Smooth 30 fps with no stutter during tab switches | [ ] |
| **File Format** | `.mp4` (H.264 / AAC) | [ ] |
| **File Size** | Under 100 MB (Ideal: 35 MB – 60 MB for easy LMS upload) | [ ] |
| **Privacy Check** | No personal email notifications, passwords, or root keys exposed | [ ] |
| **Academic Alignment**| Demonstrates live website, EC2, SSM, EBS, SG, CloudWatch, and IAM | [ ] |
