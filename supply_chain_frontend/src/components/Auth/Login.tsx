import React, { useState } from 'react';
import usePasswordToogle from './usePasswordToogle';
import { useNavigate } from 'react-router-dom';

const LogIn: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [PasswordInputType, Icon, toggleVisibility] = usePasswordToogle();
  const navigate = useNavigate();
  const [errors, setErrors] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const LoginResponse = await fetch(`${import.meta.env.VITE_BASE_API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (LoginResponse.ok) {
      const data = await LoginResponse.json();
      localStorage.setItem('token', data.token);
      navigate('/dashboard');
    } else {
      const errorData = await LoginResponse.json();
      setErrors([errorData.detail || 'Login failed, please try again']);
    }
  };

  return (
    <div id="Login" className="flex flex-col items-center justify-center mt-10 text-foreground">
      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-3 w-full max-w-sm">
        <input
          type="email"
          name="Email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="p-3 w-full rounded-md border border-input bg-background text-foreground shadow-sm"
        />

        <div className="relative w-full">
          <input
            type={PasswordInputType}
            name="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="p-3 w-full rounded-md border border-input bg-background text-foreground pr-12 shadow-sm"
          />
          <span
            className="absolute right-3 top-1/2 transform -translate-y-1/2 cursor-pointer"
            onClick={toggleVisibility}
          >
            <Icon className="w-5 h-5 text-muted-foreground" />
          </span>
        </div>

        <div className="text-sm text-muted-foreground flex justify-between w-full px-1">
          <span>Remember me</span>
          <span className="cursor-pointer hover:underline">Forgot password?</span>
        </div>

        <button
          type="submit"
          className="w-1/2 p-3 rounded-md text-white bg-blue-600 hover:bg-primary/80 transition"
        >
          Log In
        </button>

        {errors.length > 0 && (
          <div className="mt-2 text-red-500 text-sm text-center">
            {errors.map((error, index) => (
              <p key={index}>{error}</p>
            ))}
          </div>
        )}
      </form>
    </div>
  );
};

export default LogIn;
