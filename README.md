# Excess Food Management Web App

A simple web application to connect donors with surplus food to users who need it, with automatic expiry handling.

## Features

- Two user roles: Donor and User
- Donors can post food items with expiry date/time
- Users can browse available food listings with contact info
- Expired food items are automatically deleted every 10 minutes
- Authentication with email/password and JWT
- Backend in Node.js + TypeScript + Express
- SQLite database for easy local development
- Clean, modern frontend with responsive design using pure HTML, CSS, and vanilla JS

## Project Structure

excess-food-management/
│
├── public/ # Frontend static assets (HTML/CSS/JS)
│ ├── index.html # Login/Register page
│ ├── dashboard.html # Donor/User dashboard page
│ └── styles.css # Styling
│
├── src/ # Backend source code (TypeScript)
│ ├── db.ts # SQLite DB connection and helpers
│ ├── models.ts # TypeScript types (User, Food)
│ ├── authMiddleware.ts # JWT Authentication middleware
│ ├── routes/ # API route handlers
│ │ ├── auth.ts # Authentication routes (login, register)
│ │ └── foods.ts # Food CRUD routes
│ └── server.ts # Express server initialization
│
├── package.json # Node.js dependencies and scripts
├── tsconfig.json # TypeScript configuration
└── README.md # This file

text

## Prerequisites

- Node.js (v18+ recommended)
- npm or yarn package manager

## Installation

1. Clone the repository

git clone <repo-url>
cd excess-food-management

text

2. Install dependencies

npm install

or yarn install
text

## Running the Application

Start the development server (runs Express backend and serves frontend):

npm run dev

text

Open [http://localhost:4000](http://localhost:4000) in your browser.

## Usage

- Register as a donor or user.
- Donors can post food items with expiry details.
- Users can browse available (non-expired) food.
- Food uploads are automatically deleted after expiry.

## Notes

- The SQLite database file (`data.sqlite`) is generated automatically in the project root when the server runs. Do NOT commit this file to the repository.
- Expiry cleanup runs every 10 minutes, removing expired food.
- Authentication is JWT-based with token stored in localStorage on the frontend.

## Scripts

- `npm run dev` - Runs the server with hot-reloading using ts-node-dev
- `npm run build` - Compiles TypeScript to JavaScript in the `dist` folder
- `npm start` - Runs the compiled JS from `dist`

## Security

- Passwords are hashed using bcrypt.
- API routes are protected with JWT authentication.
- Never share your JWT secret key publicly.

## License

This project is open source under the MIT License.

---

Built with ❤️ using Node.js, TypeScript, Express, and SQLite.
