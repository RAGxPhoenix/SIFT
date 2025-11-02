# 🧠 SIFT-Based Feature Detection & Image Stitching

A **SIFT (Scale-Invariant Feature Transform)** based computer vision project implemented in **OpenCV (Python)** for detecting, describing, and matching image features across multiple images.  
This repository also includes **SIFT-based panoramic image stitching** — seamlessly combining overlapping images into one continuous view.  

---

## 🚀 Overview

This project demonstrates a **complete SIFT pipeline**:

1. 🕵️‍♂️ **Detects keypoints** and computes 128-D SIFT descriptors  
2. 🧩 **Matches descriptors** using Brute-Force (L2) matcher  
3. ⚖️ Applies **Lowe’s ratio test** to filter ambiguous matches  
4. 📐 Uses **RANSAC** for geometric verification via homography estimation  
5. 🖼️ **Visualizes matches** and warped image alignments  
6. 📊 Evaluates performance using key metrics (keypoints, matches, inliers, inlier ratio)  
7. 🌆 Extends to **image stitching** for seamless panorama generation  

---

## 🧩 Features

- Robust feature detection using SIFT  
- Invariance to **scale, rotation, and illumination changes**  
- RANSAC-based **homography estimation**  
- Quantitative evaluation metrics (CSV logs)  
- Multi-image **stitching module** with weighted blending  

---

## 📘 Report

📄 A detailed PDF report explaining the full pipeline, algorithms, pseudo-code, and results is included:  
👉 **[`Report.pdf`](Report.pdf)**

> ⚠️ **Important Notice:**  
> GitHub’s PDF previewer may **not display embedded images** correctly.  
> **Please download the PDF** to view all figures, visualizations, and stitched image results.  

---

## 🧰 Tech Stack

- **Language:** Python  
- **Libraries:** OpenCV, NumPy, Matplotlib  
- **Algorithms:** SIFT, Lowe’s Ratio Test, RANSAC, Homography  

---

## 🧠 Applications

- Object Recognition  
- Image Stitching / Panorama Creation  
- Structure from Motion  
- Medical Imaging Alignment  
- AR/VR Scene Reconstruction  

---

## 🧾 References

- D. Lowe, *Distinctive Image Features from Scale-Invariant Keypoints*, IJCV 2004  
- OpenCV Documentation: [https://docs.opencv.org](https://docs.opencv.org)  
- M. Fischler & R. Bolles, *RANSAC Algorithm*, 1981  

---

⭐ **If you found this project helpful, don’t forget to star the repo!**
