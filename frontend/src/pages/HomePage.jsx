import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MessageFetcher from "../components/MessageFetcher";
import logo from "/src/assets/logo.PNG";
import { useAuth0 } from "@auth0/auth0-react";

const HomePage = ({ setFirstPageVisited }) => {

    const navigate = useNavigate();
    const { loginWithRedirect, isAuthenticated, isLoading } = useAuth0();

    useEffect(() => {
        localStorage.setItem("firstPageVisited", "true");
        setFirstPageVisited(true);

        if (isAuthenticated) {
            navigate("/dashboard"); // Redirect authenticated users to dashboard
        }
    }, [isAuthenticated, navigate, setFirstPageVisited]);

    if (isLoading) return <h2>Loading...</h2>;

    return (
        <div>
            <img src="/logo.PNG" alt="logo" style={{ maxWidth: "200px", marginBottom: "1rem" }}/>
            {/* <MessageFetcher></MessageFetcher> */}
            <h1>Welcome to Talking Slides!</h1>
            <p>
                A webapp that allows you to better learn from lecture slides for lecture
                that you missed!
            </p>

            {!isAuthenticated && (
                <button onClick={() => loginWithRedirect()}>Login</button>
            )}
            <div>
            </div>
        </div>
    );
};

export default HomePage;
