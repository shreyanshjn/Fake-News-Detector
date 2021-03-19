import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import Main from './main'

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Switch>
          <Route path='/' component={Main} exact />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
