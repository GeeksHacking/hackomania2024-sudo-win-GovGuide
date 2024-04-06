import { useState } from 'react';
import { Navbar, Nav } from '@govtechsg/sgds-react/Nav';
import { Link } from 'react-router-dom'; // Import Link

function NavbarTemplate() {
  const [active, setActive] = useState('home');

  const clickNavbarItem = (eventKey: string) => {
    setActive(eventKey);
  };

  return (
    <Navbar className='navbar'>
      <Navbar.Brand as={Link} to="/">GovGuide</Navbar.Brand> {/* Use as and to for Link */}
      <Navbar.Toggle aria-controls="basic-navbar-nav"/>
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto" navbarScroll activeKey={active}>
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="/"
              eventKey="home"
              onClick={() => clickNavbarItem('home')}
            >
              Home
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              as={Link} // Use as prop
              to="/generate" // Adjust the route accordingly
              eventKey="generate"
              onClick={() => clickNavbarItem('generate')}
            >
              Generate
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavbarTemplate;