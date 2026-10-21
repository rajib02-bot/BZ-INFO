#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
============================================
THE HCKR BAZIGAR - NUMBER INFORMATION
Python Flask Server for Termux
============================================
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import re
import os
import json

app = Flask(__name__)

# ============================================
# API CONFIGURATION
# ============================================
API_URL = 
API_KEY = 

# ============================================
# HTML TEMPLATE (Complete Website)
# ============================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Bazi Gar (Hckrr) - NUMBER INFORMATION</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-x: hidden;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -webkit-touch-callout: none;
        }
        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
            -webkit-touch-callout: none;
        }
        input, textarea {
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
            user-select: text;
        }

        /* ===== DISCLAIMER POPUP ===== */
        .disclaimer-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.88);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(12px);
        }
        .disclaimer-overlay.hidden {
            opacity: 0;
            visibility: hidden;
            transition: all 0.8s ease;
        }
        .disclaimer-overlay.hide-permanent {
            display: none !important;
        }
        .disclaimer-box {
            background: linear-gradient(145deg, #0a0a2a, #15154a);
            border: 2px solid #FF9933;
            border-radius: 24px;
            padding: 45px 40px;
            max-width: 520px;
            width: 92%;
            text-align: center;
            box-shadow: 0 30px 80px rgba(0,0,0,0.6);
            animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        .disclaimer-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(255,153,51,0.05) 0%, transparent 70%);
            animation: glowRotate 10s linear infinite;
            pointer-events: none;
        }
        @keyframes glowRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes popIn {
            0% { transform: scale(0.85) translateY(40px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }
        .disclaimer-box .icon-big {
            font-size: 60px;
            margin-bottom: 10px;
            display: block;
        }
        .disclaimer-box .brand-name {
            color: #FF9933;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        .disclaimer-box h2 {
            color: #FFFFFF;
            font-size: 24px;
            font-weight: 800;
            margin: 5px 0 10px;
        }
        .disclaimer-box .divider {
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, transparent, #FF9933, transparent);
            margin: 10px auto;
            border-radius: 10px;
        }
        .disclaimer-box .content {
            color: rgba(255,255,255,0.7);
            font-size: 14px;
            line-height: 1.9;
            margin-bottom: 20px;
        }
        .disclaimer-box .content strong {
            color: #FF9933;
        }
        .disclaimer-box .btn-accept {
            padding: 14px 50px;
            background: linear-gradient(135deg, #FF9933, #e68a00);
            border: none;
            border-radius: 50px;
            color: #fff;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.3s;
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            position: relative;
            overflow: hidden;
        }
        .disclaimer-box .btn-accept::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
            transition: left 0.5s ease;
        }
        .disclaimer-box .btn-accept:hover::before {
            left: 100%;
        }
        .disclaimer-box .btn-accept:hover {
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(255,153,51,0.4);
        }
        .disclaimer-box .btn-accept i {
            margin-right: 10px;
        }

        /* ===== TRICOLOR TOP BAR ===== */
        .tricolor-bar {
            width: 100%;
            height: 6px;
            display: flex;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }
        .tricolor-bar .saffron { width: 33.33%; background: #FF9933; }
        .tricolor-bar .white { width: 33.33%; background: #FFFFFF; }
        .tricolor-bar .green { width: 33.34%; background: #138808; }

        /* ===== TOP HEADER ===== */
        .top-header {
            width: 100%;
            background: #0a0a2a;
            padding: 10px 0;
            margin-top: 6px;
            border-bottom: 2px solid #FF9933;
            position: sticky;
            top: 6px;
            z-index: 999;
        }
        .top-header .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .top-header .gov-text {
            color: #FF9933;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.5px;
        }
        .top-header .gov-text i { margin-right: 8px; color: #FFFFFF; }
        .top-header .gov-text span { color: #FFFFFF; margin: 0 10px; }
        .top-header .helpline {
            color: #FFFFFF;
            font-size: 12px;
            font-weight: 500;
            background: rgba(255,153,51,0.1);
            padding: 4px 16px;
            border-radius: 20px;
            border: 1px solid rgba(255,153,51,0.15);
        }
        .top-header .helpline i { color: #FF9933; margin-right: 8px; }

        /* ===== MAIN HEADER ===== */
        .main-header {
            width: 100%;
            background: linear-gradient(135deg, #0a0a2a 0%, #1a1a5a 50%, #0a0a2a 100%);
            padding: 20px 0;
            border-bottom: 3px solid #138808;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .main-header .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .main-header .logo-section {
            display: flex;
            align-items: center;
            gap: 18px;
        }
        .main-header .logo-img {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: 2px solid rgba(255,153,51,0.3);
            object-fit: cover;
            animation: logoFloat 3s ease-in-out infinite;
            background: rgba(255,255,255,0.05);
            padding: 3px;
            pointer-events: none;
        }
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-3px) scale(1.03); }
        }
        .main-header .title-section h1 {
            color: #FFFFFF;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }
        .main-header .title-section h1 .brand { color: #FF9933; font-weight: 800; }
        .main-header .title-section .sub-title {
            color: rgba(255,255,255,0.4);
            font-size: 12px;
            letter-spacing: 3px;
            font-weight: 400;
            text-transform: uppercase;
        }
        .main-header .status-badge {
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(255,255,255,0.05);
            padding: 8px 20px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .main-header .status-badge .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ff66;
            animation: dotPulse 1.5s ease-in-out infinite;
        }
        @keyframes dotPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.5); }
        }
        .main-header .status-badge span {
            color: rgba(255,255,255,0.4);
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1px;
        }

        /* ===== MAIN CONTAINER ===== */
        .main-container {
            max-width: 580px;
            width: 100%;
            padding: 25px 20px;
            margin: 25px 0 40px;
        }

        /* ===== CARD ===== */
        .card {
            background: #FFFFFF;
            border-radius: 20px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.06);
            overflow: hidden;
            border: 1px solid rgba(0,0,0,0.04);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 60px rgba(0,0,0,0.08);
        }
        .card-header {
            background: linear-gradient(135deg, #0a0a2a, #1a1a5a);
            padding: 25px 30px;
            border-bottom: 3px solid #FF9933;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .card-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(255,153,51,0.03) 0%, transparent 70%);
            animation: headerGlow 8s ease-in-out infinite;
        }
        @keyframes headerGlow {
            0%, 100% { transform: translate(0, 0); }
            25% { transform: translate(10%, 10%); }
            75% { transform: translate(-10%, -10%); }
        }
        .card-header .badge-gov {
            display: inline-block;
            background: rgba(255,153,51,0.12);
            padding: 5px 20px;
            border-radius: 30px;
            border: 1px solid rgba(255,153,51,0.15);
            color: #FF9933;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 12px;
            position: relative;
            z-index: 1;
        }
        .card-header .badge-gov i { margin-right: 6px; }
        .card-header .logo-icon {
            width: 75px;
            height: 75px;
            border-radius: 50%;
            border: 2px solid rgba(255,153,51,0.2);
            object-fit: cover;
            margin: 0 auto 12px;
            display: block;
            animation: iconFloat 4s ease-in-out infinite;
            background: rgba(255,255,255,0.05);
            padding: 3px;
            pointer-events: none;
        }
        @keyframes iconFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-5px) scale(1.05); }
        }
        .card-header .card-title {
            color: #FFFFFF;
            font-size: 28px;
            font-weight: 800;
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }
        .card-header .card-title .highlight { color: #FF9933; }
        .card-header .card-subtitle {
            color: rgba(255,255,255,0.35);
            font-size: 13px;
            letter-spacing: 2px;
            margin-top: 6px;
            position: relative;
            z-index: 1;
        }
        .card-header .card-subtitle i { color: #00ff66; margin-right: 6px; }
        .card-body { padding: 30px; }

        /* ===== FORM ===== */
        .form-group { margin-bottom: 18px; }
        .form-label {
            display: block;
            font-size: 12px;
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .form-label i { color: #FF9933; margin-right: 8px; }
        .input-group {
            display: flex;
            align-items: center;
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            transition: all 0.3s ease;
            overflow: hidden;
        }
        .input-group:focus-within {
            border-color: #FF9933;
            box-shadow: 0 0 0 4px rgba(255,153,51,0.08);
            background: #ffffff;
        }
        .input-group .country-code {
            padding: 14px 14px 14px 20px;
            color: #333;
            font-weight: 700;
            font-size: 15px;
            background: rgba(0,0,0,0.02);
            border-right: 1px solid #e0e0e0;
        }
        .input-group input {
            flex: 1;
            padding: 14px 18px;
            background: transparent;
            border: none;
            color: #333;
            font-size: 17px;
            outline: none;
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            font-weight: 500;
            letter-spacing: 1.5px;
        }
        .input-group input::placeholder {
            color: #aaa;
            font-weight: 400;
            font-size: 14px;
            letter-spacing: 0.5px;
        }

        /* ===== STATUS ===== */
        .status-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 6px 0 14px;
            font-size: 12px;
            color: #888;
            font-weight: 500;
        }
        .status-bar .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #138808;
            animation: pulseDot 1.5s infinite;
        }
        @keyframes pulseDot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.2; transform: scale(0.4); }
        }
        .status-bar .dot.error { background: #dc3545; }

        /* ===== BUTTON ===== */
        .btn-search {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #FF9933, #e68a00);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            letter-spacing: 1.5px;
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            position: relative;
            overflow: hidden;
        }
        .btn-search::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
            transition: left 0.6s ease;
        }
        .btn-search:hover:not(:disabled)::before { left: 100%; }
        .btn-search:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(255,153,51,0.25);
        }
        .btn-search:active:not(:disabled) { transform: translateY(0) scale(0.98); }
        .btn-search:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
        .btn-search i { font-size: 18px; }

        /* ===== RESULT ===== */
        .result-box {
            margin-top: 25px;
            border: 1px solid #e8e8e8;
            border-radius: 14px;
            overflow: hidden;
            display: none;
            background: #fafbfc;
        }
        .result-box.show {
            display: block;
            animation: slideUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes slideUp {
            0% { opacity: 0; transform: translateY(20px) scale(0.97); }
            100% { opacity: 1; transform: translateY(0) scale(1); }
        }
        .result-header {
            background: #f0f1f3;
            padding: 12px 20px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .result-header .title {
            font-size: 12px;
            font-weight: 700;
            color: #333;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .result-header .title i { color: #FF9933; margin-right: 8px; }
        .result-header .count {
            font-size: 11px;
            color: #666;
            background: #e8e8e8;
            padding: 3px 14px;
            border-radius: 20px;
            font-weight: 600;
        }
        .result-item {
            display: flex;
            padding: 14px 20px;
            border-bottom: 1px solid #f0f0f0;
            transition: all 0.2s ease;
        }
        .result-item:hover { background: #f8f9fa; }
        .result-item:last-child { border-bottom: none; }
        .result-item .label {
            color: #777;
            font-size: 11px;
            font-weight: 700;
            width: 32%;
            display: flex;
            align-items: center;
            gap: 10px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        .result-item .label i {
            font-size: 14px;
            color: #FF9933;
            width: 18px;
        }
        .result-item .value {
            color: #222;
            font-size: 14px;
            font-weight: 500;
            width: 68%;
            text-align: right;
            word-break: break-word;
        }
        .result-item .value.highlight { color: #e68a00; font-weight: 700; }
        .result-item .value.green { color: #138808; font-weight: 700; }
        .result-item .value.address { font-size: 13px; color: #555; line-height: 1.5; }

        /* ===== SECURITY BADGE ===== */
        .security-badge {
            margin-top: 18px
