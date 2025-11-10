const express = require('express');
const router = express.Router();
const db = require('../database');

// GET all attendance records
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT a.*, 
             m.first_name, m.last_name, m.email,
             ws.schedule_date, ws.start_time,
             wt.workout_name,
             c.club_name
      FROM attendance a
      JOIN members m ON a.member_id = m.member_id
      JOIN workout_schedule ws ON a.schedule_id = ws.schedule_id
      JOIN workout_types wt ON ws.workout_type_id = wt.workout_type_id
      JOIN clubs c ON ws.club_id = c.club_id
      ORDER BY a.attendance_id DESC
    `);
    res.json({
      success: true,
      count: rows.length,
      data: rows
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// GET attendance by schedule
router.get('/schedule/:schedule_id', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT a.*, m.first_name, m.last_name, m.email
      FROM attendance a
      JOIN members m ON a.member_id = m.member_id
      WHERE a.schedule_id = ?
      ORDER BY a.attendance_date DESC
    `, [req.params.schedule_id]);
    res.json({
      success: true,
      count: rows.length,
      data: rows
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// POST create attendance record (check-in)
router.post('/', async (req, res) => {
  try {
    const { schedule_id, member_id, status } = req.body;
    
    // Check if member already checked in for this schedule
    const [existing] = await db.query(
      'SELECT * FROM attendance WHERE schedule_id = ? AND member_id = ?',
      [schedule_id, member_id]
    );
    
    if (existing.length > 0) {
      return res.status(400).json({
        success: false,
        error: 'Member already checked in for this workout'
      });
    }
    
    // Check available spots
    const [schedule] = await db.query(
      'SELECT available_spots FROM workout_schedule WHERE schedule_id = ?',
      [schedule_id]
    );
    
    if (schedule.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Workout schedule not found'
      });
    }
    
    if (schedule[0].available_spots <= 0) {
      return res.status(400).json({
        success: false,
        error: 'No available spots for this workout'
      });
    }
    
    // Create attendance record
    const [result] = await db.query(
      `INSERT INTO attendance (schedule_id, member_id, status)
       VALUES (?, ?, ?)`,
      [schedule_id, member_id, status || 'Present']
    );
    
    // Update available spots
    await db.query(
      'UPDATE workout_schedule SET available_spots = available_spots - 1 WHERE schedule_id = ?',
      [schedule_id]
    );
    
    res.status(201).json({
      success: true,
      message: 'Attendance recorded successfully',
      data: { attendance_id: result.insertId }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// PUT update attendance status
router.put('/:id', async (req, res) => {
  try {
    const { status } = req.body;
    
    const [result] = await db.query(
      `UPDATE attendance 
       SET status = ?
       WHERE attendance_id = ?`,
      [status, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Attendance record not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Attendance status updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// DELETE attendance record (cancel check-in)
router.delete('/:id', async (req, res) => {
  try {
    // Get schedule_id before deleting
    const [attendance] = await db.query(
      'SELECT schedule_id FROM attendance WHERE attendance_id = ?',
      [req.params.id]
    );
    
    if (attendance.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Attendance record not found'
      });
    }
    
    const schedule_id = attendance[0].schedule_id;
    
    // Delete attendance
    const [result] = await db.query('DELETE FROM attendance WHERE attendance_id = ?', [req.params.id]);
    
    // Restore available spot
    await db.query(
      'UPDATE workout_schedule SET available_spots = available_spots + 1 WHERE schedule_id = ?',
      [schedule_id]
    );
    
    res.json({
      success: true,
      message: 'Attendance record deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
