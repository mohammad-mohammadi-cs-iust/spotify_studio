# Spotify Data Studio

A modular, object-oriented data engineering toolkit for managing and analyzing Spotify track data.

## Project Overview

This project implements a comprehensive data management system for Spotify dataset with:
- Object-oriented design with `Song` model and validation
- Polymorphic cleaning strategies (imputation and outlier handling)
- Interactive CLI dashboard
- Statistical analysis and visualization
- Robust exception handling

## Features

- **Load Dataset** – Load CSV and view missing values report
- **Clean Missing Values** – Mean, Median, or KNN imputation
- **Handle Outliers** – IQR or Z-Score methods
- **Add New Song** – Interactive input with full validation
- **Genre Insights** – Average popularity and feature analysis per genre
- **Correlation Matrix** – Identify relationships between audio features
- **Advanced Visualizations** – Bar charts, heatmaps, scatter plots, radar charts, boxplots
- **Dataset Summary** – Descriptive statistics and data quality overview

## Directory Structure
spotify_studio/
├── data/ # Dataset CSV files
├── reports/ # Generated plots and reports
│ └── generated_plots/
├── src/
│ ├── models/ # Domain models (Song)
│ ├── core/ # Constants, exceptions, validators
│ ├── services/ # Business logic services
│ ├── strategies/ # Polymorphic strategies (imputers, outlier handlers)
│ ├── cli/ # CLI dashboard
│ ├── utils/ # Utility functions
│ └── main.py # Entry point
├── requirements.txt
└── README.md


## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Place your Spotify dataset CSV in data/spotify_tracks.csv
4. Run the application:
   ```bash
   python src/main.py
   
## Usage
Navigate through the interactive menu to:
- Load and explore your dataset
- Clean missing values and handle outliers
- Add new songs with automatic validation
- Generate statistical insights and visualizations

## Technical Highlights
- Encapsulation: Song class with property setters for data validation
- Polymorphism: Abstract base classes for imputation and outlier strategies
- Separation of Concerns: Distinct modules for loading, cleaning, analysis, and visualization
- Exception Handling: Graceful error recovery without crashes
- Data Persistence: Append new songs to CSV without reloading the entire dataset

## Contributing
This project was built as a university assignment. Feel free to extend with:
- Machine learning models for popularity prediction
- Additional visualizations (word clouds, PCA, etc.)
- Web-based dashboard (Flask/Streamlit)

## License
MIT


---

## توضیحات تکمیلی

### نکات کلیدی پیاده‌سازی

1. **معماری دو لایه‌ای**: داده‌ها به صورت `DataFrame` در حافظه نگهداری می‌شوند و کلاس `Song` فقط برای اعتبارسنجی و افزودن آهنگ جدید استفاده می‌شود.

2. **چندریختی (Polymorphism)**: کلاس‌های انتزاعی `BaseImputer` و `BaseOutlierHandler` امکان افزودن الگوریتم‌های جدید را بدون تغییر در کد اصلی فراهم می‌کنند.

3. **مدیریت استثنا**: تمام خطاها در سطح `CLI` گرفته شده و پیام مناسب نمایش داده می‌شود؛ برنامه هرگز کرش نمی‌کند.

4. **اعتبارسنجی**: کلیه ویژگی‌های عددی با `property` و `setter` اعتبارسنجی می‌شوند (مثلاً محدوده ۰ تا ۱ برای ویژگی‌های صوتی).

5. **گزارش‌گیری**: امکان ذخیره نمودارها در پوشه `reports/generated_plots` برای استفاده در گزارش نهایی.

6. **امکان‌پذیری توسعه**: ساختار ماژولار باعث می‌شود به راحتی بتوان قابلیت‌های جدید اضافه کرد (مانند مدل یادگیری ماشین).

### چالش‌های فنی حل شده

1. **هماهنگی OOP و DataFrame**: انتخاب معماری دو لایه‌ای باعث شد هم از مزایای شی‌گرایی برای اعتبارسنجی استفاده شود و هم از توانمندی‌های `pandas` برای پردازش دسته‌ای.

2. **پیاده‌سازی KNN Imputer**: با استفاده از `sklearn.impute.KNNImputer` و فقط روی ستون‌های عددی، مشکل داده‌های متنی حل شد.

3. **مدیریت Outlier**: با استفاده از روش‌های clip و replace با میانه، از حذف سطرها جلوگیری شد و داده‌ها یکپارچه باقی ماندند.

4. **Append بدون بازنویسی**: با استفاده از `mode='a'` در `to_csv`، آهنگ جدید به انتهای فایل اضافه می‌شود.

---

اکنون می‌توانید این کدها را در ساختار پروژه قرار دهید و اجرا کنید. تمام نیازمندی‌های پروژه شامل OOP، چندریختی، CLI، مدیریت استثنا، تحلیل و مصورسازی به طور کامل پیاده‌سازی شده است.