-- SQL request(s)​​​​​​‌​‌​​‌​​​​‌​​​‌‌‌​​​‌‌‌​‌ below
SELECT * FROM student

-- 1. Group size (7)
SELECT * FROM student LIMIT 7

-- 2. Organized via group chat (7)
SELECT * FROM onlinechat WHERE createdat > '3961-05-05'

-- 3. Good students (7)
SELECT * FROM student ORDER BY avggrade DESC LIMIT 500

-- 4. The chemistry supply room (1)
SELECT *
FROM room LEFT JOIN roomAccessHistory
ON room.roomId = roomAccessHistory.roomId
WHERE room.roomName = 'Chemistry supply room'
AND roomAccessHistory.exitedAt - roomAccessHistory.enteredAt >= '0 01:00:00'

-- 5. No missing students (3)
SELECT * FROM schedule
WHERE schedule.day = 'Friday' AND schedule.hour = 15

-- 6. Tall mutants (2)
SELECT * FROM student
WHERE height > 300

-- 7. Nametag (1)
SELECT * FROM student
WHERE name LIKE '%M%' AND name LIKE '%W%' 

-- 8. Roommates (3)
select *, bedroomId FROM student