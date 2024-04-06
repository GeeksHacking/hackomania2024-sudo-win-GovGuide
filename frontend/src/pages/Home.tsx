import { useEffect, useState } from 'react';
import { Button } from '@govtechsg/sgds-react/Button';

function Home() {
    const [navbarHeight, setNavbarHeight] = useState(0);

    useEffect(() => {
        const updateNavbarHeight = () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                setNavbarHeight(navbar.clientHeight);
            }
        };

        updateNavbarHeight();

        window.addEventListener('resize', updateNavbarHeight);

        return () => window.removeEventListener('resize', updateNavbarHeight);
    }, []);

    // The style object for the container
    const containerStyle = {
        minHeight: `calc(100vh - ${navbarHeight + 28}px)`,
        backgroundImage: 'url("/stockphoto.jpg")', 
        backgroundSize: 'cover', 
        backgroundPosition: 'center', 
    };

    return (
        <div style={containerStyle} className="w-full overflow-auto flex flex-col justify-center">
            <div className="pl-4 md:pl-20 lg:pl-20 text-left">
                <h1 className="text-5xl">GovGuide</h1>
                <p className="italic text-xl">The newest way to find guidance in starting a business.</p>
                <Button href="/generate">Get Guidance.</Button>
            </div>
        </div>
    );
}

export default Home;
