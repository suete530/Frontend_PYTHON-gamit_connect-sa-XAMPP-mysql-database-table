<img width="1075" height="681" alt="Screenshot 2026-10-23 074214" src="https://github.com/user-attachments/assets/ff7539b2-20c6-4466-89aa-d652f4097c8f" />
<img width="1071" height="681" alt="Screenshot 2026-10-23 074154" src="https://github.com/user-attachments/assets/10986911-cdb8-4794-a2d2-39916d55b050" />

# Student Course System

Isang Python command-line application para mag-manage ng student course records gamit ang MySQL/MariaDB sa XAMPP.

## Ayos ng mga file

| File | Gamit |
| --- | --- |
| `schema.sql` | Gumagawa ng `jonard` at `student_courses` table. |
| `requirements.txt` | Python packages ng project. |
| `database.py` | MySQL connection at database queries. |
| `student.py` | Student input, validation, at CRUD operations. |
| `mainjud_ni.py` | Terminal menu at entry point ng app. |

## Requirements at setup

1. I-start ang **MySQL** sa XAMPP Control Panel.
2. Buksan ang `http://localhost/phpmyadmin`, piliin ang **Import**, at i-import ang `schema.sql`. Puwede ring patakbuhin ang SQL file gamit ang MySQL command line.
3. Buksan ang terminal sa project folder at i-install ang package:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Patakbuhin ang application:

   ```powershell
   python mainjud_ni.py
   ```

Sa unang screen, susubukan ng program ang connection at titingnan kung available ang `student_courses` table.

## MySQL settings

Default na XAMPP settings ang ginagamit: `localhost`, port `3306`, user na `root`, walang password, at database na `jonard`. Kung iba ang settings, magtakda ng environment variables bago patakbuhin. Halimbawa sa PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-password"
$env:DB_NAME = "jonard"
python mainjud_ni.py
```

Kung babaguhin ang `DB_NAME`, palitan din ang database name sa `schema.sql` bago ito i-import.

## Menu (CRUD)

- `1` — Magdagdag ng estudyante (Create)
- `2` — Tingnan lahat ng student records (Read)
- `3` — Maghanap gamit ang student number (Read)
- `4` — I-edit ang record (Update). Iwanang blangko ang field para panatilihin ang dating value.
- `5` — Magbura ng record (Delete). Kailangan munang kumpirmahin.
- `6` — Magbura ng lahat ng student records. Kailangan munang kumpirmahin.
- `0` — Lumabas

Ang student number ay unique. Bawat record ay naglalaman ng student number, pangalan, email, course/program, year level, section, edad, civil status (Single o Hindi Single), at taga saan.

Kung may existing nang `student_courses` table, patakbuhin ito sa **SQL** tab ng phpMyAdmin para maidagdag ang bagong columns:

```sql
USE jonard;
ALTER TABLE student_courses
    ADD COLUMN age TINYINT UNSIGNED NOT NULL DEFAULT 0 AFTER section,
    ADD COLUMN civil_status VARCHAR(20) NOT NULL DEFAULT 'Single' AFTER age,
    ADD COLUMN address VARCHAR(255) NOT NULL DEFAULT '' AFTER civil_status;
```
