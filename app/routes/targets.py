from flask import render_template, request, redirect, url_for, flash
from app.routes import targets_bp
from app.models import Target
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

        # Validation
        if not name or not scope:
            flash('Name and Scope are required', 'danger')
            return redirect(url_for('targets.create_target'))

        # Check if target already exists
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

        # Validation
        if not name or not scope:
            flash('Name and Scope are required', 'danger')
            return redirect(url_for('targets.edit_target', target_id=target_id))

        # Check if name is taken by another target
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