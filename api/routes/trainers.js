const express = require('express');
const router = express.Router();
const db = require('../database');

// GET all trainers
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT t.*, c.club_name 
      FROM trainers t
      LEFT JOIN clubs c ON t.club_id = c.club_id
      ORDER BY t.trainer_id DESC
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

// GET trainer by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT t.*, c.club_name 
      FROM trainers t
      LEFT JOIN clubs c ON t.club_id = c.club_id
      WHERE t.trainer_id = ?
    `, [req.params.id]);
    
    if (rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Trainer not found'
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

// GET trainer's schedule
router.get('/:id/schedule', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT ws.*, wt.workout_name, c.club_name
      FROM workout_schedule ws
      JOIN workout_types wt ON ws.workout_type_id = wt.workout_type_id
      JOIN clubs c ON ws.club_id = c.club_id
      WHERE ws.trainer_id = ?
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

// POST create new trainer
router.post('/', async (req, res) => {
  try {
    const { first_name, last_name, email, phone, specialization, certification, hire_date, club_id } = req.body;
    
    const [result] = await db.query(
      `INSERT INTO trainers (first_name, last_name, email, phone, specialization, certification, hire_date, club_id)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [first_name, last_name, email, phone, specialization, certification, hire_date, club_id]
    );
    
    res.status(201).json({
      success: true,
      message: 'Trainer created successfully',
      data: { trainer_id: result.insertId }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// PUT update trainer
router.put('/:id', async (req, res) => {
  try {
    const { first_name, last_name, email, phone, specialization, certification, club_id } = req.body;
    
    const [result] = await db.query(
      `UPDATE trainers 
       SET first_name = ?, last_name = ?, email = ?, phone = ?, specialization = ?, certification = ?, club_id = ?
       WHERE trainer_id = ?`,
      [first_name, last_name, email, phone, specialization, certification, club_id, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Trainer not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Trainer updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// DELETE trainer
router.delete('/:id', async (req, res) => {
  try {
    const [result] = await db.query('DELETE FROM trainers WHERE trainer_id = ?', [req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Trainer not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Trainer deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
