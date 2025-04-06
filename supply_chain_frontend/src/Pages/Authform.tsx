import React, { useState } from 'react';
import SignUp from '../components/Auth/SignUp';
import Login from '../components/Auth/Login';

const AuthForm: React.FC = () => {
  const [isLoginPage, setIsLoginPage] = useState(true);

  const toggleForm = () => setIsLoginPage(prev => !prev);

  return (
    <div className="flex items-center justify-center min-h-screen bg-[hsl(var(--background))] text-[hsl(var(--foreground))]">
      <div className="relative flex w-[800px] overflow-hidden rounded-[30px] bg-[hsl(var(--card))] shadow-lg">
        <div className="relative p-5 transition-all duration-500 ease-in-out w-[65%]">
          <h1 className="text-2xl font-bold mb-4">{isLoginPage ? 'Log In' : 'Sign Up'}</h1>
          {isLoginPage ? <Login /> : <SignUp onSuccess={toggleForm} />}
        </div>

        <div className="absolute top-0 right-0 w-[35%] h-full p-2.5 flex flex-col justify-center items-center text-center uppercase rounded-[200px_0_0_200px] transition-all duration-500 ease-in-out bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))]">
          <h1 className="text-lg font-bold">{isLoginPage ? 'Welcome Back!' : 'Hello Friend!'}</h1>
          <p className="text-sm mt-2">
            {isLoginPage
              ? 'Enter your personal details to use this site'
              : 'Register with your personal details to get started'}
          </p>
          <button
            onClick={toggleForm}
            className="mt-2 py-2 w-[150px] border border-white bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))] transition"
          >
            {isLoginPage ? 'Sign Up' : 'Log In'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
