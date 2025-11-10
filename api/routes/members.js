const express = require('express');
const router = express.Router();
const db = require('../database');

// GET all members
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT * FROM members ORDER BY member_id DESC');
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

// GET member by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT * FROM members WHERE member_id = ?', [req.params.id]);
    if (rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Member not found'
      });
    }
    res.json({
      success: true,
      data: rows[0]
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// GET member's active memberships
router.get('/:id/memberships', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT m.*, c.club_name 
      FROM memberships m
      JOIN clubs c ON m.club_id = c.club_id
      WHERE m.member_id = ?
      ORDER BY m.start_date DESC
    `, [req.params.id]);
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

// GET member's attendance history
router.get('/:id/attendance', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT a.*, ws.schedule_date, ws.start_time, wt.workout_name
      FROM attendance a
      JOIN workout_schedule ws ON a.schedule_id = ws.schedule_id
      JOIN workout_types wt ON ws.workout_type_id = wt.workout_type_id
      WHERE a.member_id = ?
      ORDER BY ws.schedule_date DESC, ws.start_time DESC
    `, [req.params.id]);
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

// POST create new member
router.post('/', async (req, res) => {
  try {
    const { first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone, registration_date } = req.body;
    
    const [result] = await db.query(
      `INSERT INTO members (first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone, registration_date)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone, registration_date]
    );
    
    res.status(201).json({
      success: true,
      message: 'Member created successfully',
      data: { member_id: result.insertId }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// PUT update member
router.put('/:id', async (req, res) => {
  try {
    const { first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone } = req.body;
    
    const [result] = await db.query(
      `UPDATE members 
       SET first_name = ?, last_name = ?, email = ?, phone = ?, date_of_birth = ?, gender = ?, address = ?, emergency_contact = ?, emergency_phone = ?
       WHERE member_id = ?`,
      [first_name, last_name, email, phone, date_of_birth, gender, address, emergency_contact, emergency_phone, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Member not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Member updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// DELETE member
router.delete('/:id', async (req, res) => {
  try {
    const [result] = await db.query('DELETE FROM members WHERE member_id = ?', [req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Member not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Member deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
