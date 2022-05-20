import logo from './logo.svg';
import './App.css';
import Home from './component/Home';
import Buses from './component/Buses';
import Login from './component/Login';
import myReducer from './reducers/UserReducer';
import 'bootstrap/dist/css/bootstrap.min.css';

export const UserContext = createContext()

function App() {
  const [user, dispatch] = useReducer(myReducer)

  return (
    <BrowserRouter>
    <UserContext.Provider value={[user, dispatch]}>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/route/:routeId/buses" element={<Buses />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      <Footer />
    </UserContext.Provider>
  </BrowserRouter>
  );
}

export default App;
