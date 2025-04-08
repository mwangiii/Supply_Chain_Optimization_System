import { useState } from 'react';

const usePasswordToggle = (): [string, React.ReactNode, () => void] => {
  const [visible, setVisible] = useState(false);

  // Use React.ReactNode instead of JSX.Element
  const Icon = visible ? (
    <span role="img" aria-label="Hide password">
      👁️
    </span>
  ) : (
    <span role="img" aria-label="Show password">
      👁️‍🗨️
    </span>
  );

  const toggleVisibility = () => setVisible((prev) => !prev);

  return [visible ? 'text' : 'password', Icon, toggleVisibility];
};

export default usePasswordToggle;
