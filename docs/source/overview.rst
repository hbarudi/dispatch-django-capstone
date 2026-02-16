Overview
========

Dispatch Django is a role-based news platform built with Django. Content is created by
journalists and published only after editor approval.

Roles
-----

- **Administrator**: full site management via Django Admin.
- **Editor**: reviews and approves/unpublishes articles, manages publishers.
- **Journalist**: authors articles and newsletters.
- **Reader**: subscribes to publishers/journalists and consumes curated content.

High-level workflow
-------------------

1. Journalist creates an Article (initially unapproved).
2. Editor approves the Article.
3. Approved content becomes visible in the public feed.
