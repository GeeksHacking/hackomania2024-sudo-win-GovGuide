import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import NavbarTemplate from './components/Nav';

function App() {
  return (
    <>
      <NavbarTemplate />
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
