type WordUpdateListener = () => void;

let listeners: WordUpdateListener[] = [];

export const subscribeToWordUpdates = (listener: WordUpdateListener) => {
  listeners.push(listener);
  return () => {
    listeners = listeners.filter(l => l !== listener);
  };
};

export const notifyWordUpdates = () => {
  listeners.forEach(listener => listener());
}; 