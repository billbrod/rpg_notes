# RPG Notes

Try keeping notes in markdown so we can build them into a website.

The notes are found in the `docs/` folder, and are all markdown files. They can
be edited in the browser or locally.

## Development

(These are my notes as to how I got this set up, not necessary for anyone else)

We deploy to netlify so that we can hide the DM-only notes behind a login. The
website is deployed to Netlify using the action `.github/workflows/deploy.yml`.
We use the Netlify Identity widget to handle logins, which required the
following steps:
- [enable identity](https://docs.netlify.com/visitor-access/identity/) via the
  integrations tab
- Creating the actual login button is done as discussed
  [here](https://www.netlify.com/blog/2018/01/23/getting-started-with-jwt-and-identity/),
  adding extra javascript and overriding the announce block to add the actual
  login button itself.
- set registration to invite-only under `Site configuration > Identity >
  Registration`.
  
Then, to add users:
- Go to `Integrations > Identity`, to invite users and set their role
- They'll get an email, which they should follow and will prompt them to create
  a password
  - I also configured this to accept Github authentication.
  
The actual hiding of information is done via [role-based
redirects](https://docs.netlify.com/visitor-access/role-based-access-control/),
as defined in the `netlify.toml` file in this repo. Anyone who doesn't have the
role `dm` will only see a "404" page when they go to `/dm` on the website.
