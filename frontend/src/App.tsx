import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import NavbarTemplate from './components/Nav';
import Generate from './pages/Generate';

function App() {
  return (
    <>
      <NavbarTemplate />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate" element={<Generate />} />
      </Routes>
    </>
  );
}

export default App;
