import { useEffect, useState } from "react";
import "../userProfile.css";

const emptyProfile = {
  primary_role: "",
  target_role: "",
  experience_level: "",
  education: [],
  skills: [],
  projects: [],
  experience: [],
  certifications: [],
};

const UserProfile = () => {
  const [profile, setProfile] = useState(emptyProfile);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("accessToken");

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await fetch("http://localhost:8000/accounts/profile/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        setProfile({
          ...emptyProfile,
          ...data.profile,
        });
      } else {
        setMessage(data.message || "Failed to load profile.");
      }
    } catch (error) {
      console.error(error);
      setMessage("Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setProfile((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const addItem = (field) => {
    setProfile((prev) => ({
      ...prev,
      [field]: [...prev[field], ""],
    }));
  };

  const updateItem = (field, index, value) => {
    setProfile((prev) => {
      const updated = [...prev[field]];
      updated[index] = value;

      return {
        ...prev,
        [field]: updated,
      };
    });
  };

  const removeItem = (field, index) => {
    setProfile((prev) => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSaving(true);
    setMessage("");

    try {
      const response = await fetch(
        "http://localhost:8000/accounts/profile/update/",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(profile),
        },
      );

      const data = await response.json();

      if (response.ok) {
        setProfile({
          ...emptyProfile,
          ...data.profile,
        });

        setMessage("Profile updated successfully.");
      } else {
        setMessage(data.message || "Failed to update profile.");
      }
    } catch (error) {
      console.error(error);
      setMessage("Something went wrong.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="profile-loading">
        <div className="profile-loader"></div>
        <p>Loading your profile...</p>
      </div>
    );
  }

  return (
    <main className="profile-page">
      {/* Header */}
      <section className="profile-hero">
        <div className="profile-hero-icon">
          <span>✦</span>
        </div>

        <div>
          <p className="profile-eyebrow">PERSONAL PROFILE</p>

          <h1>
            Build your <span>career profile.</span>
          </h1>

          <p className="profile-description">
            Keep your skills, experience and career goals updated. This
            information helps power your AI career guidance, interviews and
            recommendations.
          </p>
        </div>
      </section>

      <form onSubmit={handleSubmit} className="profile-form">
        {/* Basic Information */}
        <ProfileCard
          number="01"
          title="Career Overview"
          description="Tell us where you are now and where you want to go."
        >
          <div className="profile-grid">
            <ProfileField
              label="Current Role"
              name="primary_role"
              value={profile.primary_role}
              onChange={handleChange}
              placeholder="Computer Engineering Student"
            />

            <ProfileField
              label="Target Role"
              name="target_role"
              value={profile.target_role}
              onChange={handleChange}
              placeholder="Software Engineer"
            />

            <div className="profile-field">
              <label>Experience Level</label>

              <select
                name="experience_level"
                value={profile.experience_level}
                onChange={handleChange}
              >
                <option value="">Select experience level</option>
                <option value="none">No Experience</option>
                <option value="intern">Intern</option>
                <option value="junior">Junior</option>
                <option value="mid_level">Mid-level</option>
                <option value="senior">Senior</option>
              </select>
            </div>
          </div>
        </ProfileCard>

        {/* Education */}
        <ProfileCard
          number="02"
          title="Education"
          description="Add your academic background."
          action={<AddButton onClick={() => addItem("education")} />}
        >
          <RepeatableList
            field="education"
            items={profile.education}
            updateItem={updateItem}
            removeItem={removeItem}
            placeholder="B.E. Computer Engineering — XYZ University"
          />
        </ProfileCard>

        {/* Skills */}
        <ProfileCard
          number="03"
          title="Skills"
          description="Add technologies and professional skills you know."
          action={<AddButton onClick={() => addItem("skills")} />}
        >
          <div className="skill-list">
            {profile.skills.length === 0 ? (
              <EmptyState text="No skills added yet." />
            ) : (
              profile.skills.map((skill, index) => (
                <div className="skill-item" key={index}>
                  <span className="skill-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <input
                    value={
                      typeof skill === "string"
                        ? skill
                        : Object.values(skill || {}).join(" • ")
                    }
                    onChange={(e) =>
                      updateItem("skills", index, e.target.value)
                    }
                    placeholder="e.g. Python"
                  />

                  <RemoveButton onClick={() => removeItem("skills", index)} />
                </div>
              ))
            )}
          </div>
        </ProfileCard>

        {/* Projects */}
        <ProfileCard
          number="04"
          title="Projects"
          description="Showcase projects that demonstrate your abilities."
          action={<AddButton onClick={() => addItem("projects")} />}
        >
          <RepeatableList
            field="projects"
            items={profile.projects}
            updateItem={updateItem}
            removeItem={removeItem}
            placeholder="AI Interview & Examination System"
          />
        </ProfileCard>

        {/* Experience */}
        <ProfileCard
          number="05"
          title="Work Experience"
          description="Add internships, jobs or other professional experience."
          action={<AddButton onClick={() => addItem("experience")} />}
        >
          <RepeatableList
            field="experience"
            items={profile.experience}
            updateItem={updateItem}
            removeItem={removeItem}
            placeholder="Software Engineering Intern — ABC Technologies"
          />
        </ProfileCard>

        {/* Certifications */}
        <ProfileCard
          number="06"
          title="Certifications"
          description="Add certificates and professional credentials."
          action={<AddButton onClick={() => addItem("certifications")} />}
        >
          <RepeatableList
            field="certifications"
            items={profile.certifications}
            updateItem={updateItem}
            removeItem={removeItem}
            placeholder="Python Programming Certification"
          />
        </ProfileCard>

        {/* Save Area */}
        <div className="profile-save">
          <div className="profile-save-info">
            <span className="save-dot"></span>

            <div>
              <strong>Your profile is private</strong>
              <p>Your information is used to personalize your experience.</p>
            </div>
          </div>

          <button
            type="submit"
            className="profile-save-button"
            disabled={saving}
          >
            {saving ? (
              <>
                <span className="button-spinner"></span>
                Saving...
              </>
            ) : (
              <>
                Save Changes
                <span>→</span>
              </>
            )}
          </button>
        </div>

        {message && (
          <div
            className={`profile-message ${
              message.includes("successfully") ? "success" : "error"
            }`}
          >
            {message}
          </div>
        )}
      </form>
    </main>
  );
};

/* =========================================
   COMPONENTS
========================================= */

const ProfileCard = ({ number, title, description, action, children }) => {
  return (
    <section className="profile-card">
      <div className="profile-card-header">
        <div className="profile-card-title">
          <span className="profile-card-number">{number}</span>

          <div>
            <h2>{title}</h2>
            <p>{description}</p>
          </div>
        </div>

        {action}
      </div>

      <div className="profile-card-content">{children}</div>
    </section>
  );
};

const ProfileField = ({ label, name, value, onChange, placeholder }) => {
  return (
    <div className="profile-field">
      <label>{label}</label>

      <input
        type="text"
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
      />
    </div>
  );
};

const RepeatableList = ({
  field,
  items,
  updateItem,
  removeItem,
  placeholder,
}) => {
  if (items.length === 0) {
    return <EmptyState text="Nothing added yet. Click + Add to get started." />;
  }

  return (
    <div className="repeatable-list">
      {items.map((item, index) => {
        const displayValue =
          typeof item === "string"
            ? item
            : Object.values(item || {})
                .filter(Boolean)
                .join(" • ");

        return (
          <div className="repeatable-item" key={index}>
            <span className="repeatable-index">
              {String(index + 1).padStart(2, "0")}
            </span>

            <input
              type="text"
              value={displayValue}
              onChange={(e) => updateItem(field, index, e.target.value)}
              placeholder={placeholder}
            />

            <RemoveButton onClick={() => removeItem(field, index)} />
          </div>
        );
      })}
    </div>
  );
};

const AddButton = ({ onClick }) => {
  return (
    <button type="button" className="profile-add-button" onClick={onClick}>
      <span>+</span>
      Add
    </button>
  );
};

const RemoveButton = ({ onClick }) => {
  return (
    <button
      type="button"
      className="profile-remove-button"
      onClick={onClick}
      title="Remove"
    >
      ×
    </button>
  );
};

const EmptyState = ({ text }) => {
  return (
    <div className="profile-empty">
      <span>＋</span>
      <p>{text}</p>
    </div>
  );
};

export default UserProfile;
