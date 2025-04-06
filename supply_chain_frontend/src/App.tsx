import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import AuthForm from "./Pages/Authform";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/" element={<AuthForm />} />
            </Routes>
        </Router>
    )

  }

export default App;