import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const HomePage = ({ setFirstPageVisited }) => {

    const navigate = useNavigate();

    useEffect(() => {
        localStorage.setItem("firstPageVisited", "true");
        setFirstPageVisited(true);
      }, [setFirstPageVisited]);
    

    // Function to handle location selection
    const handleLocationSelect = (location) => {
        console.log("Selected location:", location);
    };

    return (
        <div>
            
            <h1>Welcome!</h1>
            <button onClick={() => navigate("/dashboard")}>Navigate to Dashboard</button>
        </div>
    );
};

export default HomePage;
