import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ErrorNotification from "../ErrorNotification";
import { useCreateGardensMutation } from "../app/authApi";

function GardenForm() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [error, setError] = useState("");
  const [createGarden, result] = useCreateGardensMutation();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await createGarden({ name, location });
      navigate("/gardens");
    } catch (error) {
      setError(error.message);
    }
  }

  return (
    <div className="row">
      <div className="offset-3 col-6">
        <div className="shadow p-4 mt-4">
          <h1>Create a Garden</h1>
          <ErrorNotification error={error} />
          <form onSubmit={handleSubmit}>
            <div className="form-floating mb-3">
              <input
                placeholder="Garden Name"
                required
                type="text"
                name="name"
                id="name"
                value={name || ""}
                onChange={(e) => setName(e.target.value)}
                className="form-control"
              />
              <label htmlFor="name">Name</label>
            </div>
            <div className="form-floating mb-3">
              <textarea
                placeholder="Garden Location"
                required
                type="text"
                name="location"
                id="location"
                value={location || ""}
                onChange={(e) => setLocation(e.target.value)}
                className="form-control"
              ></textarea>
              <label htmlFor="location">Location</label>
            </div>
            <button className="btn btn-success">Create</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default GardenForm;
