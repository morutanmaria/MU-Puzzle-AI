Project Overview

This project implements an interactive version of the MU puzzle introduced by Douglas Hofstadter in Gödel, Escher, Bach.

The MU puzzle is a formal rewriting system based on four syntactic rules over the alphabet:

{ M, I, U }

Starting from the initial string:

MI

The central question is:

Can we derive MU using only the four formal rules?

This project provides:

A complete implementation of the MU system

A graphical interface for interactive rewriting

Explicit rule-based transformations

Invariant tracking (mod-3 property)

Optional integration with Mace4 for automated model finding

The MU System Rules

Let x denote any string after the leading M.

Rule 1:
If a string ends with I, you may append U.

xI → xIU

Rule 2:
If a string has the form Mx, you may double x.

Mx → Mxx

Rule 3:
Replace any occurrence of III with U.

III → U

Rule 4:
Remove any occurrence of UU.

UU → ε

Project Features
 Interactive GUI

Click directly on highlighted substrings (III, UU) to apply transformations

Rule buttons (R1–R4) for explicit rule application

Undo functionality

Clean visual layout

Large string display

 Multiple Rule Application Sites

If a rule applies in multiple places (e.g., MIIII has two III occurrences), the GUI allows the user to click the exact location to transform.

This models a proper term rewriting system.

 Mathematical Invariant Tracking

The system continuously displays:

I mod 3
This reflects the key invariant of the MU puzzle:

The number of I symbols modulo 3 is preserved under all rules.

Since:

MI contains 1 I

MU contains 0 I

And 1 mod 3 ≠ 0 mod 3, it follows that:

MU is not derivable from MI.

Mace4 Integration

The project can optionally integrate with
Mace4.

Mace4 is a finite model finder developed by
William McCune.

Purpose in this project

Instead of brute-force search, Mace4 is used to:

Construct a finite model

Show that all MU rules hold

Demonstrate that MU is not reachable

This provides an automated formal proof of impossibility.

Architecture

Python GUI runs on Windows

Mace4 runs on Linux (via WSL)

Python generates .in file

Mace4 is executed via subprocess

Output is parsed and shown in GUI

This separation reflects standard formal methods workflows.

How to Run
Install Python 3

Ensure Python 3.10+ is installed.

Run the GUI
python gui.py

Theoretical Significance

The MU puzzle demonstrates:

Formal systems

Rewriting systems

Invariants

Undecidability intuition

Model-theoretic reasoning

It serves as an accessible introduction to:

First-order logic

Automated reasoning

Model finding

Proof by invariant

Screenshots: 

<img width="787" height="595" alt="Screenshot 2026-02-28 215057" src="https://github.com/user-attachments/assets/6e9ff364-9494-4c3d-aff5-957b583dc798" />
<img width="792" height="590" alt="Screenshot 2026-02-28 215140" src="https://github.com/user-attachments/assets/dd33e500-7f10-40c9-ab20-b39cdcacd975" />
<img width="787" height="590" alt="Screenshot 2026-02-28 215222" src="https://github.com/user-attachments/assets/d0db00f6-4a3d-43ca-9644-472cbe04558a" />


