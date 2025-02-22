import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MessageFetcher from "../components/MessageFetcher";

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
            <img src="/logo.PNG" alt="logo" style={{ maxWidth: "200px", marginBottom: "1rem" }}/>
            {/* <MessageFetcher></MessageFetcher> */}
            <h1>Welcome to Talking Slides!</h1>
            <p>
                A webapp that allows you to better learn from lecture slides for lecture
                that you missed!
            </p>
            <div>
                <button onClick={() => navigate("/dashboard")} style={{ marginRight: "0.5rem" }}>
                Log in
                </button>
            </div>
        </div>
    );
};

export default HomePage;
