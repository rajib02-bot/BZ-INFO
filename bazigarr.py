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
API_URL = "https://bazigar-api.onrender.com/api/v1/lookup"
API_KEY = "bazigar-here"

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
            padding: 14px;
            background: #f8f9fa;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 25px;
            flex-wrap: wrap;
            border: 1px solid #e8e8e8;
        }
        .security-badge .badge-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
            color: #555;
            font-weight: 500;        }
        .security-badge .badge-item i { color: #138808; font-size: 15px; }

        /* ===== SOCIAL MEDIA ===== */
        .social-section {
            margin-top: 18px;
            padding: 18px;
            background: #f8f9fa;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #e8e8e8;
        }
        .social-section .social-title {
            font-size: 11px;
            color: #777;
            margin-bottom: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        .social-section .social-title i { color: #FF9933; margin-right: 8px; }
        .social-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
            flex-wrap: wrap;
        }
        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 22px;
            border-radius: 50px;
            text-decoration: none;
            color: #fff;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s ease;
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
            position: relative;
            overflow: hidden;
        }
        .social-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s ease;
        }
        .social-btn:hover::before { left: 100%; }
        .social-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        .social-btn i { font-size: 18px; }
        .social-btn.youtube { background: #FF0000; }
        .social-btn.instagram { background: linear-gradient(135deg, #833AB4, #FD1D1D, #F56040); }
        .social-btn.telegram { background: #0088cc; }

        /* ===== JSON TOGGLE ===== */
        .json-toggle {
            margin-top: 14px;
            padding: 12px;
            background: transparent;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            color: #888;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            font-family: 'Noto Sans Devanagari', 'Segoe UI', Arial, sans-serif;
        }
        .json-toggle:hover {
            background: #f8f9fa;
            border-color: #FF9933;
            color: #FF9933;
        }
        .json-toggle i { font-size: 14px; }
        .json-box {
            margin-top: 12px;
            background: #0a0a0a;
            border-radius: 10px;
            padding: 14px;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            color: #00ff66;
            display: none;
            max-height: 200px;
            overflow: auto;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.8;
            border: 1px solid rgba(0,255,102,0.05);
        }
        .json-box.show {
            display: block;
            animation: slideUp 0.3s ease;
        }
        .json-box::-webkit-scrollbar { width: 4px; }
        .json-box::-webkit-scrollbar-thumb { background: rgba(0,255,102,0.15); border-radius: 4px; }

        /* ===== FOOTER ===== */
        .footer-section {
            width: 100%;
            background: #0a0a2a;
            border-top: 3px solid #FF9933;
            padding: 25px 0;
            margin-top: 20px;
        }
        .footer-section .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            text-align: center;
        }
        .footer-section .footer-links {
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }
        .footer-section .footer-links a {
            color: rgba(255,255,255,0.25);
            font-size: 11px;
            text-decoration: none;
            transition: all 0.3s ease;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        .footer-section .footer-links a:hover { color: #FF9933; }
        .footer-section .footer-links a i { margin-right: 6px; }
        .footer-section .copyright {
            color: rgba(255,255,255,0.08);
            font-size: 10px;
            letter-spacing: 2px;
            font-weight: 300;
        }
        .footer-section .copyright .brand-name { color: #FF9933; font-weight: 600; }
        .footer-section .tricolor-footer {
            width: 100%;
            height: 4px;
            display: flex;
            margin-top: 18px;
        }
        .footer-section .tricolor-footer .saffron { width: 33.33%; background: #FF9933; }
        .footer-section .tricolor-footer .white { width: 33.33%; background: #FFFFFF; }
        .footer-section .tricolor-footer .green { width: 33.34%; background: #138808; }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .main-header .title-section h1 { font-size: 18px; }
            .main-header .title-section .sub-title { font-size: 9px; letter-spacing: 1.5px; }
            .main-header .logo-img { width: 50px; height: 50px; }
            .main-header .status-badge { padding: 5px 14px; }
            .main-header .status-badge span { font-size: 9px; }
            .top-header .gov-text { font-size: 10px; }
            .top-header .helpline { font-size: 10px; padding: 3px 12px; }
            .card-header .card-title { font-size: 22px; }
            .card-body { padding: 20px; }
            .card-header { padding: 20px; }
            .card-header .logo-icon { width: 60px; height: 60px; }
            .result-item { flex-wrap: wrap; padding: 12px 16px; }
            .result-item .label { width: 100%; margin-bottom: 4px; }
            .result-item .value { width: 100%; text-align: left; }
            .security-badge { gap: 12px; padding: 12px; }
            .security-badge .badge-item { font-size: 10px; }
            .social-btn { padding: 8px 16px; font-size: 12px; }
            .social-btn i { font-size: 15px; }
            .disclaimer-box { padding: 30px 22px; }
            .disclaimer-box h2 { font-size: 20px; }
            .disclaimer-box .icon-big { font-size: 50px; }
            .disclaimer-box .content { font-size: 13px; }
            .footer-section .footer-links { gap: 15px; }
            .footer-section .footer-links a { font-size: 10px; }
        }
        @media (max-width: 480px) {
            .main-header .title-section h1 { font-size: 15px; }
            .main-header .logo-img { width: 42px; height: 42px; }
            .card-header .card-title { font-size: 18px; }
            .main-container { padding: 15px 12px; }
            .card-body { padding: 16px; }
            .result-item .value { font-size: 13px; }
            .social-buttons { gap: 10px; }
            .social-btn { padding: 7px 14px; font-size: 11px; }
            .top-header .container { flex-direction: column; text-align: center; }
            .card-header .logo-icon { width: 50px; height: 50px; }
        }

        /* ===== ERROR ===== */
        .error-text {
            color: #dc3545;
            font-size: 12px;
            padding: 6px 0;
            display: none;
            font-weight: 500;
        }
        .error-text.show {
            display: block;
            animation: shake 0.4s ease;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-6px); }
            75% { transform: translateX(6px); }
        }

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #f0f0f0; }
        ::-webkit-scrollbar-thumb { background: #FF9933; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #e68a00; }

        /* ===== DISABLE COPY ===== */
        img, svg, video {
            -webkit-user-drag: none;
            user-drag: none;
            pointer-events: none;
        }
    </style>
</head>
<body>

<!-- ===== DISCLAIMER POPUP ===== -->
<div class="disclaimer-overlay" id="disclaimerOverlay">
    <div class="disclaimer-box">
        <span class="icon-big">🛡️</span>
        <div class="brand-name">The Hckrr BaziGar</div>
        <h2>DISCLAIMER</h2>
        <div class="divider"></div>
        <div class="content">
            This tool is for <strong>educational and security awareness</strong> purposes only.<br>
            All data is obtained from <strong>publicly available sources</strong>.<br><br>
            <i class="fas fa-link" style="color:#FF9933;"></i> Use responsibly &amp; ethically.
        </div>
        <button class="btn-accept" onclick="acceptDisclaimer()">
            <i class="fas fa-check-circle"></i> I UNDERSTAND
        </button>
    </div>
</div>

<!-- ===== TRICOLOR TOP BAR ===== -->
<div class="tricolor-bar">
    <div class="saffron"></div>
    <div class="white"></div>
    <div class="green"></div>
</div>

<!-- ===== TOP HEADER ===== -->
<div class="top-header">
    <div class="container">
        <div class="gov-text">
            <i class="fas fa-shield-halved"></i>
            The Hckrr BaziGar <span>|</span> CYBER SECURITY DIVISION
        </div>
        <div class="helpline">
            <i class="fas fa-phone"></i> <strong>Helpline: +91 7029538584</strong>
        </div>
    </div>
</div>

<!-- ===== MAIN HEADER ===== -->
<div class="main-header">
    <div class="container">
        <div class="logo-section">
            <img src="https://i.postimg.cc/1VBJWPhR/IMG-20260724-232723-958.webp" alt="Anish Exploits Logo" class="logo-img" draggable="false">
            <div class="title-section">
                <h1>
                    <span class="brand">The Hacker</span> Bazi Garr
                </h1>
                <div class="sub-title">🔴 OSINT · SECURITY RESEARCH · INTELLIGENCE</div>
            </div>
        </div>
        <div class="status-badge">
            <div class="dot"></div>
            <span>SYSTEM ACTIVE</span>
        </div>
    </div>
</div>

<!-- ===== MAIN CONTAINER ===== -->
<div class="main-container">

    <div class="card">

        <!-- Card Header -->
        <div class="card-header">
            <div class="badge-gov">
                <i class="fas fa-lock"></i> SECURE · ENCRYPTED
            </div>
            <img src="https://i.postimg.cc/1VBJWPhR/IMG-20260724-232723-958.webp" alt="Anish Exploits Logo" class="logo-icon" draggable="false">
            <div class="card-title">
                <span class="highlight">NUMBER</span> INFORMATION
            </div>
            <div class="card-subtitle">
                <i class="fas fa-shield"></i>
                Advanced Phone Number Intelligence System
            </div>
        </div>

        <!-- Card Body -->
        <div class="card-body">

            <!-- Form -->
            <form id="trackForm">
                <div class="form-group">
                    <label class="form-label">
                        <i class="fas fa-phone"></i> Enter 10-Digit Mobile Number
                    </label>
                    <div class="input-group">
                        <span class="country-code">+91</span>
                        <input type="tel" id="phoneInput" placeholder="Enter phone number" maxlength="10" inputmode="numeric" value="">
                    </div>
                </div>

                <div class="status-bar">
                    <span class="dot" id="statusDot"></span>
                    <span id="statusText">Ready to track</span>
                </div>

                <div class="error-text" id="errorText">❌ Error message</div>

                <button type="submit" class="btn-search" id="trackBtn">
                    <i class="fas fa-search"></i> GET INFORMATION
                </button>
            </form>

            <!-- Result -->
            <div class="result-box" id="resultBox">
                <div class="result-header">
                    <div class="title">
                        <i class="fas fa-file-alt"></i> Citizen Information
                    </div>
                    <div class="count">
                        <i class="fas fa-database"></i> <span id="recordCount">0</span> Record(s)
                    </div>
                </div>
                <div id="resultContent"></div>
            </div>

            <!-- Security Badge -->
            <div class="security-badge">
                <div class="badge-item"><i class="fas fa-lock"></i> SSL Secure</div>
                <div class="badge-item"><i class="fas fa-shield-halved"></i> The Hckrr BaziGar</div>
                <div class="badge-item"><i class="fas fa-check-circle"></i> Verified</div>
                <div class="badge-item"><i class="fas fa-clock"></i> 24x7 Service</div>
            </div>

            <!-- API Info -->
            <div id="apiInfo" style="display:none; margin-top:14px; padding:12px; background:#f8f9fa; border-radius:10px; display:flex; justify-content:center; gap:25px; flex-wrap:wrap; font-size:11px; color:#666; border:1px solid #e8e8e8;"></div>

            <!-- Social Media -->
            <div class="social-section">
                <div class="social-title"><i class="fas fa-share-alt"></i> The Hckrr BaziGar</div>
                <div class="social-buttons">
                    <a href="https://bazigar-protfollio.netlify.app/" target="_blank" class="social-btn youtube"><i class="fab fa-youtube"></i> YouTube</a>
                    <a href="https://instagram.com/hckr__rajib" target="_blank" class="social-btn instagram"><i class="fab fa-instagram"></i> Instagram</a>
                    <a href="https://t.me/hckr_BaziGarr" target="_blank" class="social-btn telegram"><i class="fab fa-telegram-plane"></i> Telegram</a>
                </div>
            </div>

            <!-- JSON Toggle -->
            <button class="json-toggle" onclick="toggleJson()">
                <i class="fas fa-code"></i> View Raw Data (JSON)
            </button>

            <div class="json-box" id="jsonBox"></div>

        </div>
    </div>

</div>

<!-- ===== FOOTER ===== -->
<div class="footer-section">
    <div class="container">
        <div class="footer-links">
            <a href="#"><i class="fas fa-info-circle"></i> About The Hckrr BaziGar</a>
            <a href="#"><i class="fas fa-shield-halved"></i> Privacy Policy</a>
            <a href="#"><i class="fas fa-gavel"></i> Terms & Conditions</a>
            <a href="https://t.me/hckr_BaziGarr" target="_blank"><i class="fas fa-headset"></i> Support</a>
            <a href="tel:+916209856775"><i class="fas fa-phone"></i> Contact</a>
        </div>
        <div class="copyright">
            © 2024 <span class="brand-name">The Hckrr BaziGarr</span> · All Rights Reserved
        </div>
        <div class="tricolor-footer">
            <div class="saffron"></div>
            <div class="white"></div>
            <div class="green"></div>
        </div>
    </div>
</div>

<!-- ===== JAVASCRIPT ===== -->
<script>
// ============================================
// DISCLAIMER - ONLY ONCE
// ============================================
(function() {
    if (sessionStorage.getItem('disclaimerShown') === 'true') {
        document.getElementById('disclaimerOverlay').classList.add('hide-permanent');
    }
})();

function acceptDisclaimer() {
    sessionStorage.setItem('disclaimerShown', 'true');
    document.getElementById('disclaimerOverlay').classList.add('hidden');
    setTimeout(function() {
        document.getElementById('disclaimerOverlay').classList.add('hide-permanent');
    }, 800);
}

// ============================================
// TOGGLE JSON
// ============================================
function toggleJson() {
    const box = document.getElementById('jsonBox');
    box.classList.toggle('show');
    if (box.classList.contains('show')) {
        box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// ============================================
// CALL API - USING PROXY
// ============================================
async function callAPI(number) {
    try {
        // Use Flask proxy endpoint
        const response = await fetch('/api/lookup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ number: number })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📦 API Response:', data);
        return data;
        
    } catch (error) {
        console.error('❌ API Error:', error);
        return { status: 'error', message: error.message };
    }
}

// ============================================
// DISPLAY RESULTS
// ============================================
function displayResults(number, data) {
    const resultBox = document.getElementById('resultBox');
    const resultContent = document.getElementById('resultContent');
    const recordCount = document.getElementById('recordCount');
    const apiInfo = document.getElementById('apiInfo');
    const jsonBox = document.getElementById('jsonBox');
    
    jsonBox.textContent = JSON.stringify(data, null, 2);
    
    if (data.status === 'error') {
        resultBox.classList.remove('show');
        document.getElementById('errorText').textContent = '❌ ' + (data.message || 'API Error');
        document.getElementById('errorText').classList.add('show');
        return;
    }
    
    if (data.result && data.result.length > 0) {
        const results = data.result;
        const totalRecords = results.length;
        
        recordCount.textContent = totalRecords;
        
        let html = '';
        const info = results[0];
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-phone"></i> Phone</span>
            <span class="value highlight">${info.num || '+91 ' + number}</span>
        </div>`;
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-user"></i> Full Name</span>
            <span class="value highlight">${info.name || 'N/A'}</span>
        </div>`;
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-user-tie"></i> Father's Name</span>
            <span class="value">${info.fname || 'N/A'}</span>
        </div>`;
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-id-card"></i> Aadhaar Number</span>
            <span class="value green">${info.aadhar || 'N/A'}</span>
        </div>`;
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-map-pin"></i> Address</span>
            <span class="value address">${info.address || 'N/A'}</span>
        </div>`;
        
        html += `<div class="result-item">
            <span class="label"><i class="fas fa-signal"></i> Network 
            <span class="value">${info.circle || 'N/A'}</span>
        </div>`;
        
        if (info.alt) {
            html += `<div class="result-item">
                <span class="label"><i class="fas fa-phone-plus"></i> Alternate Number</span>
                <span class="value">${info.alt}</span>
            </div>`;
        }
        
        if (info.email) {
            html += `<div class="result-item">
                <span class="label"><i class="fas fa-envelope"></i> Email</span>
                <span class="value">${info.email}</span>
            </div>`;
        }
        
        resultContent.innerHTML = html;
        resultBox.classList.add('show');
        document.getElementById('errorText').classList.remove('show');
        
        let apiHtml = '';
        if (data.BUY_API) {
            apiHtml += `<span><i class="fas fa-shopping-cart" style="color:#FF9933;"></i> BUY API: <strong>${data.BUY_API}</strong></span>`;
        }
        if (data.SUPPORT) {
            apiHtml += `<span><i class="fas fa-headset" style="color:#FF9933;"></i> SUPPORT: <strong>${data.SUPPORT}</strong></span>`;
        }
        if (apiHtml) {
            apiInfo.innerHTML = apiHtml;
            apiInfo.style.display = 'flex';
        }
        
    } else {
        resultBox.classList.remove('show');
        document.getElementById('errorText').textContent = '❌ No data found for this number!';
        document.getElementById('errorText').classList.add('show');
    }
}

// ============================================
// SEARCH FUNCTION
// ============================================
async function searchNumber() {
    const input = document.getElementById('phoneInput');
    const number = input.value.trim();
    const statusText = document.getElementById('statusText');
    const statusDot = document.getElementById('statusDot');
    const trackBtn = document.getElementById('trackBtn');
    const errorText = document.getElementById('errorText');
    
    if (!number || number.length !== 10 || !/^[0-9]{10}$/.test(number)) {
        errorText.textContent = '⚠️ Please enter a valid 10-digit phone number!';
        errorText.classList.add('show');
        return;
    }
    
    errorText.classList.remove('show');
    
    trackBtn.disabled = true;
    trackBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SEARCHING...';
    statusText.textContent = '🔍 Searching...';
    statusDot.className = 'dot';
    
    document.getElementById('resultBox').classList.remove('show');
    document.getElementById('apiInfo').style.display = 'none';
    
    try {
        const data = await callAPI(number);
        displayResults(number, data);
        
        if (data.status === 'success' && data.result && data.result.length > 0) {
            statusText.textContent = '✅ Search completed (' + data.result.length + ' records found)';
            statusDot.className = 'dot';
        } else if (data.status === 'error') {
            statusText.textContent = '❌ API Error';
            statusDot.className = 'dot error';
        } else {
            statusText.textContent = '❌ No data found';
            statusDot.className = 'dot error';
        }
        
    } catch (error) {
        console.error('Search Error:', error);
        statusText.textContent = '❌ Connection error';
        statusDot.className = 'dot error';
        errorText.textContent = '❌ Network error. Please try again.';
        errorText.classList.add('show');
    }
    
    trackBtn.disabled = false;
    trackBtn.innerHTML = '<i class="fas fa-search"></i> GET INFORMATION';
}

// ============================================
// EVENT LISTENERS
// ============================================
document.getElementById('trackForm').addEventListener('submit', function(e) {
    e.preventDefault();
    searchNumber();
});

document.getElementById('phoneInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        searchNumber();
    }
});

document.getElementById('phoneInput').addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

// ============================================
// DISABLE COPY
// ============================================
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
});

document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && (e.key === 'c' || e.key === 'v' || e.key === 's' || e.key === 'p' || e.key === 'u')) {
        e.preventDefault();
        return false;
    }
    if (e.key === 'F12') {
        e.preventDefault();
        return false;
    }
});

document.addEventListener('dragstart', function(e) {
    e.preventDefault();
    return false;
});

// ============================================
// AUTO SEARCH
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        searchNumber();
    }, 1500);
});
</script>

</body>
</html>
'''

# ============================================
# FLASK ROUTE: HOME PAGE
# ============================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# ============================================
# FLASK ROUTE: API LOOKUP (PROXY)
# ============================================
@app.route('/api/lookup', methods=['POST'])
def lookup():
    try:
        data = request.get_json()
        number = data.get('number', '').strip()
        
        if not number:
            return jsonify({"status": "error", "message": "Phone number required"})
        
        # Clean number
        clean_number = re.sub(r'[\+\s\-]', '', number)
        
        # Build API URL
        params = {
            'key': API_KEY,
            'type': 'number',
            'num': clean_number
        }
        
        # Call API
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        
        api_data = response.json()
        
        # Check if API returned error
        if api_data.get('status') == 'error':
            return jsonify(api_data)
        
        # Format response
        return jsonify({
            "status": "success",
            "result": api_data.get('result', [])
        })
        
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "API timeout"})
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"API error: {str(e)}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"})

# ============================================
# MAIN: RUN SERVER
# ============================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print("\n" + "="*50)
    print("🛡️  The Hckrr BaziGarS - NUMBER INFORMATION")
    print("="*50)
    print(f"✅ Server running on: http://127.0.0.1:{port}")
    print(f"📱 Open in browser: http://127.0.0.1:{port}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
            
