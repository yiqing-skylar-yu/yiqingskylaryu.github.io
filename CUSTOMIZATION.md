# Customizing The Website

This file explains where common settings live. You do not need to know HTML, CSS, or JavaScript for routine content edits.

## Pages

Edit these files for public page text:

- `index.qmd`: homepage name, position, scholarly framing, and short overview sections
- `research.qmd`: research themes, projects, methods, and trajectory
- `teaching.qmd`: teaching philosophy, courses, materials, effectiveness, and teachable courses
- `mentoring.qmd`: mentoring philosophy, process, evidence, and development priorities
- `publications.qmd`: publication page introduction and section headings
- `cv.qmd`: living CV page text and CV link

## Publications

Edit `data/publications.yml`.

This is the single publication source of truth. The Publications page renders from that YAML file through `pub-listing.ejs` and `pub-listing.css`.

## Teaching Materials

Edit `data/teaching-materials.yml`.

Add public files in `files/teaching-materials/` only after removing private student details, internal course-management notes, and copyrighted material that should not be public.

## Research Projects And Courses

These simple data files preserve reusable source information:

- `data/research-projects.yml`
- `data/courses.yml`

The current pages are intentionally text-forward, so after changing a data file, check whether the corresponding public page should also be updated.

## Site Title And Name

Edit `_quarto.yml`.

Look for:

```yaml
website:
  title: "Yiqing Skylar Yu"
```

## Navigation

Edit `_quarto.yml`.

Look for:

```yaml
navbar:
```

Keep the main navigation focused on Home, Research, Teaching, Mentoring, Publications, and CV unless the site grows later.

## Links

Edit `_quarto.yml` for navbar and footer links.

Edit `cv.qmd` for the living CV link.

Edit `index.qmd`, `publications.qmd`, or `cv.qmd` if you want to change page-level Google Scholar or email links.

## Headshot

Replace `images/headshot.jpg`.

Keep the filename the same, or update the image path in `index.qmd`.

## Colors

Edit `styles.css`.

Most colors are near the top:

```css
:root {
  --skylar-ink: #243230;
  --skylar-muted: #66726f;
  --skylar-line: #e4e8e6;
  --skylar-accent: #2f6f68;
  --skylar-accent-dark: #1d514c;
  --skylar-bg: #fbfbfa;
}
```

Use one restrained accent color so the site stays close to the academic template.

## Typography And Spacing

Edit `styles.css`.

Useful starting points:

```css
body {
  font-size: 17px;
  line-height: 1.68;
}

:root {
  --skylar-prose: 820px;
}
```

## What Not To Edit Unless You Are Comfortable

Avoid changing:

- the `project:` section in `_quarto.yml`
- the `format:` section in `_quarto.yml`
- the generated `docs/` folder
- generated preview folders such as `_site/` or `.quarto/`
