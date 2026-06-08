from flask import render_template, request, redirect, url_for, flash
from app.routes import targets_bp
from app.models import Target, Note, Endpoint
from app import db


@targets_bp.route('/targets')
def list_targets():
    """List all targets with filter by status"""
    status_filter = request.args.get('status', 'all')

    if status_filter == 'all':
        targets = Target.query.order_by(Target.created_at.desc()).all()
    else:
        targets = Target.query.filter_by(status=status_filter).order_by(Target.created_at.desc()).all()

    return render_template('targets/list.html', targets=targets, current_status=status_filter)


@targets_bp.route('/targets/create', methods=['GET', 'POST'])
def create_target():
    """Create new target"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        scope = request.form.get('scope', '').strip()
        out_of_scope = request.form.get('out_of_scope', '').strip()
        status = request.form.get('status', 'active')
        priority = request.form.get('priority', '3')

        if not name or not scope:
            flash('Name and Scope are required', 'danger')
            return redirect(url_for('targets.create_target'))

        if Target.query.filter_by(name=name).first():
            flash('Target with this name already exists', 'danger')
            return redirect(url_for('targets.create_target'))

        try:
            target = Target(
                name=name,
                description=description,
                scope=scope,
                out_of_scope=out_of_scope,
                status=status,
                priority=int(priority)
            )
            db.session.add(target)
            db.session.commit()
            flash(f'Target "{name}" created successfully', 'success')
            return redirect(url_for('targets.view_target', target_id=target.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating target: {str(e)}', 'danger')
            return redirect(url_for('targets.create_target'))

    return render_template('targets/create.html')


@targets_bp.route('/targets/<int:target_id>')
def view_target(target_id):
    """View target detail"""
    target = Target.query.get_or_404(target_id)
    return render_template('targets/detail.html', target=target)


@targets_bp.route('/targets/<int:target_id>/edit', methods=['GET', 'POST'])
def edit_target(target_id):
    """Edit target"""
    target = Target.query.get_or_404(target_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        scope = request.form.get('scope', '').strip()
        out_of_scope = request.form.get('out_of_scope', '').strip()
        status = request.form.get('status', 'active')
        priority = request.form.get('priority', '3')

        if not name or not scope:
            flash('Name and Scope are required', 'danger')
            return redirect(url_for('targets.edit_target', target_id=target_id))

        if name != target.name and Target.query.filter_by(name=name).first():
            flash('Target with this name already exists', 'danger')
            return redirect(url_for('targets.edit_target', target_id=target_id))

        try:
            target.name = name
            target.description = description
            target.scope = scope
            target.out_of_scope = out_of_scope
            target.status = status
            target.priority = int(priority)
            db.session.commit()
            flash(f'Target "{name}" updated successfully', 'success')
            return redirect(url_for('targets.view_target', target_id=target_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating target: {str(e)}', 'danger')
            return redirect(url_for('targets.edit_target', target_id=target_id))

    return render_template('targets/create.html', target=target)


@targets_bp.route('/targets/<int:target_id>/delete', methods=['POST'])
def delete_target(target_id):
    """Delete target"""
    target = Target.query.get_or_404(target_id)
    target_name = target.name

    try:
        db.session.delete(target)
        db.session.commit()
        flash(f'Target "{target_name}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting target: {str(e)}', 'danger')

    return redirect(url_for('targets.list_targets'))


@targets_bp.route('/targets/<int:target_id>/status/<new_status>', methods=['POST'])
def change_target_status(target_id, new_status):
    """Quick change target status"""
    target = Target.query.get_or_404(target_id)

    valid_statuses = ['active', 'paused', 'completed']
    if new_status not in valid_statuses:
        flash('Invalid status', 'danger')
        return redirect(url_for('targets.view_target', target_id=target_id))

    try:
        target.status = new_status
        db.session.commit()
        flash(f'Target status changed to "{new_status}"', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error changing status: {str(e)}', 'danger')

    return redirect(url_for('targets.view_target', target_id=target_id))


@targets_bp.route('/targets/<int:target_id>/notes/create', methods=['POST'])
def create_note(target_id):
    """Create new note for target"""
    target = Target.query.get_or_404(target_id)

    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    note_type = request.form.get('note_type', 'general')
    is_pinned = request.form.get('is_pinned') == 'on'

    if not title or not content:
        flash('Title and Content are required', 'danger')
        return redirect(url_for('targets.view_target', target_id=target_id))

    try:
        note = Note(
            target_id=target_id,
            title=title,
            content=content,
            note_type=note_type,
            is_pinned=is_pinned
        )
        db.session.add(note)
        db.session.commit()
        flash(f'Note "{title}" created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating note: {str(e)}', 'danger')

    return redirect(url_for('targets.view_target', target_id=target_id))


@targets_bp.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """Delete note"""
    note = Note.query.get_or_404(note_id)
    target_id = note.target_id
    note_title = note.title

    try:
        db.session.delete(note)
        db.session.commit()
        flash(f'Note "{note_title}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting note: {str(e)}', 'danger')

    return redirect(url_for('targets.view_target', target_id=target_id))


@targets_bp.route('/targets/<int:target_id>/endpoints/create', methods=['POST'])
def create_endpoint(target_id):
    """Create new endpoint for target"""
    target = Target.query.get_or_404(target_id)

    url = request.form.get('url', '').strip()
    http_method = request.form.get('http_method', 'GET')
    status_code = request.form.get('status_code', '').strip()
    is_authenticated = request.form.get('is_authenticated') == 'on'
    tech_stack = request.form.get('tech_stack', '').strip()
    notes = request.form.get('notes', '').strip()

    if not url:
        flash('URL is required', 'danger')
        return redirect(url_for('targets.view_target', target_id=target_id))

    existing = Endpoint.query.filter_by(
        target_id=target_id,
        url=url,
        http_method=http_method
    ).first()

    if existing:
        flash('This endpoint already exists for this target', 'warning')
        return redirect(url_for('targets.view_target', target_id=target_id))

    try:
        status_code_int = None
        if status_code:
            status_code_int = int(status_code)

        endpoint = Endpoint(
            target_id=target_id,
            url=url,
            http_method=http_method,
            status_code=status_code_int,
            is_authenticated=is_authenticated,
            tech_stack=tech_stack if tech_stack else None,
            notes=notes if notes else None
        )
        db.session.add(endpoint)
        db.session.commit()
        flash(f'Endpoint "{http_method} {url}" created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating endpoint: {str(e)}', 'danger')

    return redirect(url_for('targets.view_target', target_id=target_id))


@targets_bp.route('/endpoints/<int:endpoint_id>/delete', methods=['POST'])
def delete_endpoint(endpoint_id):
    """Delete endpoint"""
    endpoint = Endpoint.query.get_or_404(endpoint_id)
    target_id = endpoint.target_id
    endpoint_str = f"{endpoint.http_method} {endpoint.url}"

    try:
        db.session.delete(endpoint)
        db.session.commit()
        flash(f'Endpoint "{endpoint_str}" deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting endpoint: {str(e)}', 'danger')

    return redirect(url_for('targets.view_target', target_id=target_id))