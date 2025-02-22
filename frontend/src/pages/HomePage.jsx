import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const HomePage = ({ setFirstPageVisited }) => {

    const navigate = useNavigate();

    useEffect(() => {
        localStorage.setItem("firstPageVisited", "true");
        setFirstPageVisited(true);
      }, [setFirstPageVisited]);

    return (
        <div>
            
            <h1>Welcome!</h1>
            <button onClick={() => navigate("/dashboard")}>Go</button>
        </div>
    );
};

export default HomePage;
