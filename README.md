# RPG Notes

Try keeping notes in markdown so we can build them into a website.

The notes are found in the `docs/` folder, and are all markdown files.

## Development

(These are my notes as to how I got this set up, not necessary for anyone else)

We deploy to netlify so that we can hide the DM-only notes behind a login. The
website is deployed to Netlify using the action `.github/workflows/deploy.yml`.
We use the Netlify Identity widget to handle logins, which required the
following steps:
- [enable identity](https://docs.netlify.com/visitor-access/identity/) via the
  integrations tab
- Then, from `Integrations > Identity`, can invite users and set their role.
- Creating the actual login button is done as discussed
  [here](https://www.netlify.com/blog/2018/01/23/getting-started-with-jwt-and-identity/),
  adding extra javascript and overriding the announce block to add the actual
  login button itself.
