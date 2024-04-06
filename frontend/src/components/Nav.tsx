import { useState, useEffect } from "react";
import { Navbar, Nav } from "@govtechsg/sgds-react/Nav";
import { Link, useLocation } from "react-router-dom"; // Import Link
import GovGuideLogo from "@/assets/GovGuide.png";

function NavbarTemplate() {
  const location = useLocation();
  const [active, setActive] = useState("home");

  const pathMapper: { [key: string]: string } = {
    "/": "home",
    "/generate": "generate",
  };

  useEffect(() => {
    setActive(pathMapper[location.pathname] || "home");
  }, [location.pathname]);

  const clickNavbarItem = (eventKey: string) => {
    setActive(eventKey);
  };

  return (
    <Navbar className="navbar" expand={"md"}>
      <Navbar.Brand as={Link} to="/">
        <img
          src={GovGuideLogo}
          alt="GovGuide"
          className="w-[80px] h-[80px] p-2.5"
        />
      </Navbar.Brand>
      {/* Use as and to for Link */}
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto" navbarScroll activeKey={active}>
          <Nav.Item>
            <Nav.Link
              as={Link}
              to="/"
              eventKey="home"
              onClick={() => clickNavbarItem("home")}
            >
              Home
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link
              as={Link} // Use as prop
              to="/generate" // Adjust the route accordingly
              eventKey="generate"
              onClick={() => clickNavbarItem("generate")}
            >
              Generate
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default NavbarTemplate;
