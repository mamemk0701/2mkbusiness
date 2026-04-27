import { useEffect, useState } from 'react';
import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const stored = localStorage.getItem('gripforce_theme') || 'light';
    setTheme(stored);
  }, []);

  const toggle = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    localStorage.setItem('gripforce_theme', next);
    if (next === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <button
      onClick={toggle}
      aria-label={`Passer en mode ${theme === 'light' ? 'sombre' : 'clair'}`}
      className="relative w-9 h-9 md:w-10 md:h-10 rounded-full border border-ink-200 dark:border-ink-700 hover:border-ink-400 dark:hover:border-ink-500 transition-colors flex items-center justify-center group"
    >
      <Sun
        size={16}
        className={`absolute transition-all duration-300 ${
          theme === 'light' ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 rotate-90 scale-50'
        }`}
      />
      <Moon
        size={16}
        className={`absolute transition-all duration-300 ${
          theme === 'dark' ? 'opacity-100 rotate-0 scale-100' : 'opacity-0 -rotate-90 scale-50'
        }`}
      />
    </button>
  );
}
