# Mini SQL Sandbox

A lightweight web-based SQL sandbox to interact with a local SQLite database.  
Execute queries, view tables, and explore SQL commands in a terminal-style interface right in your browser.

## Features

- Run SQL queries directly from the web interface.
- Display query results in a neat, styled table.
- Help section with example queries:
  - `SELECT * FROM enrichment;`
  - `SELECT Term, p_value FROM enrichment;`
  - `SELECT * FROM enrichment WHERE adj_p_value <= 0.05;`
  - `SELECT * FROM enrichment ORDER BY odds_ratio DESC;`
  - `SELECT COUNT(*) FROM enrichment;`
  - `SELECT Genes FROM enrichment WHERE Genes LIKE '%UBC%';`
  - `SELECT * FROM enrichment LIMIT 10;`
  - `SELECT * FROM enrichment WHERE id = 1;`
  - `DROP TABLE enrichment;`
  - `ALTER TABLE enrichment ADD COLUMN new_col_name DATA_TYPE;`
  - `ALTER TABLE enrichment RENAME COLUMN old_col_name TO renamed_col_name;`
  - `INSERT INTO enrichment (Term, p_value, Genes) VALUES ('example', 0.01, 'UBC');`
- Terminal-like interface with animated matrix background.
- Syntax highlighting for queries in the help section.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python, Flask  
- **Database:** SQLite  

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AqeebAkeel/mini-sql-sandbox.git
cd mini-sql-sandbox
