-- 1. Most borrowed books

SELECT b.title,
       COUNT(br.borrow_id) AS borrow_count
FROM books b
JOIN borrow_records br
ON b.book_id = br.book_id
GROUP BY b.book_id, b.title
ORDER BY borrow_count DESC;


-- 2. Members who borrowed more than 3 books

SELECT m.name,
       COUNT(br.borrow_id) AS total_borrowed
FROM members m
JOIN borrow_records br
ON m.member_id = br.member_id
GROUP BY m.member_id, m.name
HAVING COUNT(br.borrow_id) > 3;


-- 3. Count books by category

SELECT category,
       COUNT(*) AS total_books
FROM books
GROUP BY category;


-- 4. Currently borrowed books

SELECT b.title,
       m.name,
       br.borrow_date
FROM borrow_records br
JOIN books b
ON br.book_id = b.book_id
JOIN members m
ON br.member_id = m.member_id
WHERE br.status = 'Borrowed';


-- 5. Total books available in library

SELECT SUM(available_copies) AS total_available_books
FROM books;
