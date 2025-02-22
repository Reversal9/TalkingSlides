import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const HomePage = ({ setFirstPageVisited }) => {

    const navigate = useNavigate();
    const [username, setUsername] = useState(""); 
    const [password, setPassword] = useState(""); 

    useEffect(() => {
        localStorage.setItem("firstPageVisited", "true");
        setFirstPageVisited(true);
    }, [setFirstPageVisited]);

    return (
        <div>
            <h1>Welcome to Talking Slides!</h1>
            <p>
                A webapp that allows you to better learn from lecture slides for lecture
                that you missed!
            </p>
            <input
                className="textinput"
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{
                padding: "0.5rem",
                margin: "1rem 0",
                fontSize: "1rem",
                borderRadius: "4px",
                border: "1px solid #ccc",
                }}
            />
            <input
                className="textinput"
                type="text"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                padding: "0.5rem",
                margin: "1rem 0",
                fontSize: "1rem",
                borderRadius: "4px",
                border: "1px solid #ccc",
                }}
            />
            <div>
                <button onClick={() => navigate("/dashboard")} style={{ marginRight: "0.5rem" }}>
                Log in
                </button>
                <button onClick={() => navigate("/dashboard")}>Sign up</button>
            </div>
        </div>
    );
};

export default HomePage;
