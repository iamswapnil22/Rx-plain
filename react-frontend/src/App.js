import './App.css';

function App() {
  return (
    <div className="App">
      <nav className="navbar">
        <h1>Dashboard</h1>
      </nav>
      <main className="main-content">
        <div className="card">
          <h2>Welcome</h2>
          <p>This is a simple and clean dashboard interface.</p>
        </div>
        <div className="card">
          <h2>Statistics</h2>
          <div className="stat-grid">
            <div className="stat-item">
              <h3>Users</h3>
              <p>1,234</p>
            </div>
            <div className="stat-item">
              <h3>Products</h3>
              <p>56</p>
            </div>
            <div className="stat-item">
              <h3>Orders</h3>
              <p>789</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
