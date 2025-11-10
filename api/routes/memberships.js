const express = require('express');
const router = express.Router();
const db = require('../database');

// GET all memberships
router.get('/', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT ms.*, m.first_name, m.last_name, m.email, c.club_name
      FROM memberships ms
      JOIN members m ON ms.member_id = m.member_id
      JOIN clubs c ON ms.club_id = c.club_id
      ORDER BY ms.membership_id DESC
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

// GET active memberships only
router.get('/active', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT ms.*, m.first_name, m.last_name, m.email, c.club_name
      FROM memberships ms
      JOIN members m ON ms.member_id = m.member_id
      JOIN clubs c ON ms.club_id = c.club_id
      WHERE ms.status = 'Active'
      ORDER BY ms.end_date ASC
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

// GET membership by ID
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await db.query(`
      SELECT ms.*, m.first_name, m.last_name, m.email, c.club_name
      FROM memberships ms
      JOIN members m ON ms.member_id = m.member_id
      JOIN clubs c ON ms.club_id = c.club_id
      WHERE ms.membership_id = ?
    `, [req.params.id]);
    
    if (rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Membership not found'
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

// POST create new membership
router.post('/', async (req, res) => {
  try {
    const { member_id, club_id, membership_type, start_date, end_date, price, status } = req.body;
    
    const [result] = await db.query(
      `INSERT INTO memberships (member_id, club_id, membership_type, start_date, end_date, price, status)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [member_id, club_id, membership_type, start_date, end_date, price, status || 'Active']
    );
    
    res.status(201).json({
      success: true,
      message: 'Membership created successfully',
      data: { membership_id: result.insertId }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// PUT update membership
router.put('/:id', async (req, res) => {
  try {
    const { membership_type, start_date, end_date, price, status } = req.body;
    
    const [result] = await db.query(
      `UPDATE memberships 
       SET membership_type = ?, start_date = ?, end_date = ?, price = ?, status = ?
       WHERE membership_id = ?`,
      [membership_type, start_date, end_date, price, status, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Membership not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Membership updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// DELETE membership
router.delete('/:id', async (req, res) => {
  try {
    const [result] = await db.query('DELETE FROM memberships WHERE membership_id = ?', [req.params.id]);
    
    if (result.affectedRows === 0) {
      return res.status(404).json({
        success: false,
        error: 'Membership not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Membership deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
