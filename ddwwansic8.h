#ifndef _DDWWANSIC8_H
#define _DDWWANSIC8_H
/* SccsID = %W% %G%   */

#ifdef __cplusplus
extern         "C" {
#endif

	int32_t    ddagroup (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t albuf, void *buffer, uint32_t *leng);
	int32_t    ddagroup_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *albuf, void *buffer, uint32_t *leng, uint64_t lname);
	int32_t    ddainfo (int32_t *error, int32_t diaref, char *name, uint32_t *sizes, int32_t *adim, int32_t *index);
	int32_t    ddainfo_ (int32_t *error, int32_t *diaref, char *name, uint32_t *sizes, int32_t *adim, int32_t *index, uint64_t lname);
	int32_t    ddainfo2 (int32_t *error, int32_t diaref, char *name, uint32_t *ntval, uint32_t *sizes, int32_t *adim, char *aname, int32_t *narea);
	int32_t    ddainfo2_ (int32_t *error, int32_t *diaref, char *name, uint32_t *ntval, uint32_t *sizes, int32_t *adim, char *aname, int32_t *narea, uint64_t lname, uint64_t laname);
	int32_t    ddcalib_ (int32_t *ier, int32_t *diaref, char *name, uint32_t *type, uint32_t *vl, float *pdat, char *dim, uint64_t lname, uint64_t ldim);
	int32_t    ddccsgnl (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddccsgnl_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddccsgrp (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddccsgrp_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddccxsig (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t *indices, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddccxsig_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *indices, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddclose (int32_t *error, int32_t diaref);
	int32_t    ddclose_ (int32_t *error, int32_t *diaref);
	int32_t    ddcsgnl (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddcsgnl_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddcsgrp (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddcsgrp_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddcxsig (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t *indices, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim);
	int32_t    ddcxsig_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *indices, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, int32_t *ncal, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddcshotnr (char *exper, char *diag, uint32_t shot, uint32_t *cshot);
	int32_t    ddcshotnr_ (char *exper, char *diag, uint32_t *shot, uint32_t *cshot, uint64_t lexper, uint64_t ldiag);
	int32_t    dddelay (int32_t *error, int32_t diaref, char *name, uint32_t type, void *delay);
	int32_t    dddelay_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, void *delay, uint64_t lname);
	int32_t    dddim (int32_t *error, int32_t physunit, char *physdim);
	int32_t    dddim_ (int32_t *error, int32_t *physunit, char *physdim, uint64_t lphysdim);
	int32_t    ddevent (int32_t *error, int32_t diaref, char *name, int32_t codetyp, void *code, uint32_t type, void *value, float *freq, uint64_t lg2);
	int32_t    ddevent_ (int32_t *error, int32_t *diaref, char *name, int32_t *codetyp, void *code, uint32_t *type, void *value, float *freq, uint64_t lname, uint64_t lg2);
	int32_t    ddflist (int32_t *error, int32_t diaref, int32_t lbuf, int32_t *buffer, int32_t *length);
	int32_t    ddflist_ (int32_t *error, int32_t *diaref, int32_t *lbuf, int32_t *buffer, int32_t *length);
	int32_t    ddgetaug (int32_t argc, void *argv[]);
	int32_t    dddgetsgr (int32_t *error, char *exper, char *diag, uint32_t shot, int32_t edition, char *name, double time1, double time2, char *timebase, double *timebuf, double *buffer, uint32_t *length, uint32_t *indices, uint32_t anzsig, char *physdim);
	int32_t    dddgetsgr_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, char *name, double *time1, double *time2, char *timebase, double *timebuf, double *buffer, uint32_t *length, uint32_t *indices, uint32_t *anzsig, char *physdim,
			          uint64_t lexper, uint64_t ldiag, uint64_t lname, uint64_t ltimebase, uint64_t lphysdim);
	int32_t    dddgetsig (int32_t *error, char *exper, char *diag, uint32_t shot, int32_t edition, char *name, double time1, double time2, char *timebase, double *timebuf, double *buffer, uint32_t *length, uint32_t anzsig, char *physdim);
	int32_t    dddgetsig_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, char *name, double *time1, double *time2, char *timebase, double *timebuf, double *buffer, uint32_t *length, uint32_t *anzsig, char *physdim,
			          uint64_t lexper, uint64_t ldiag, uint64_t lname, uint64_t ltimebase, uint64_t lphysdim);
	int32_t    ddgetsgr (int32_t *error, char *exper, char *diag, uint32_t shot, int32_t edition, char *name, float time1, float time2, char *timebase, float *timebuf, float *buffer, uint32_t *length, uint32_t *indices, uint32_t anzsig, char *physdim);
	int32_t    ddgetsgr_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, char *name, float *time1, float *time2, char *timebase, float *timebuf, float *buffer, uint32_t *length, uint32_t *indices, uint32_t *anzsig, char *physdim,
			          uint64_t lexper, uint64_t ldiag, uint64_t lname, uint64_t ltimebase, uint64_t lphysdim);
	int32_t    ddgetsig (int32_t *error, char *exper, char *diag, uint32_t shot, int32_t edition, char *name, float time1, float time2, char *timebase, float *timebuf, float *buffer, uint32_t *length, uint32_t anzsig, char *physdim);
	int32_t    ddgetsig_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, char *name, float *time1, float *time2, char *timebase, float *timebuf, float *buffer, uint32_t *length, uint32_t *anzsig, char *physdim,
			          uint64_t lexper, uint64_t ldiag, uint64_t lname, uint64_t ltimebase, uint64_t lphysdim);
	int32_t    ddlastshotnr (int32_t *error, uint32_t *shotnr);
	int32_t    ddlastshotnr_ (int32_t *error, uint32_t *shotnr);
	int32_t    ddlnames (int32_t *error, int32_t diaref, char *name, int32_t *listlen, char *nlist);
	int32_t    ddlnames_ (int32_t *error, int32_t *diaref, char *name, int32_t *listlen, char *nlist, uint64_t lname, uint64_t lnlist);
	int32_t    ddmapinfo (int32_t *error, int32_t diaref, char *name, uint32_t *indices, char *devname, int32_t *chan);
	int32_t    ddmapinfo_ (int32_t *error, int32_t *diaref, char *name, uint32_t *indices, char *devname, int32_t *chan, uint64_t lname, uint64_t ldevname);
	int32_t    ddobjdata (int32_t *error, int32_t diaref, char *name, int32_t lbuf, void *buffer, uint32_t *lengb);
	int32_t    ddobjdata_ (int32_t *error, int32_t *diaref, char *name, int32_t *lbuf, void *buffer, uint32_t *lengb, uint64_t lname);
	int32_t    ddobjhdr (int32_t *error, int32_t diaref, char *name, int32_t *obuf, char *otext);
	int32_t    ddobjhdr_ (int32_t *error, int32_t *diaref, char *name, int32_t *obuf, char *otext, uint64_t lname, uint64_t lotext);
	int32_t    ddobjname (int32_t *error, int32_t diaref, int32_t object, char *name);
	int32_t    ddobjname_ (int32_t *error, int32_t *diaref, int32_t *object, char *name, uint64_t lname);
	int32_t    ddobjval (int32_t *error, int32_t diaref, char *name, char *field, int32_t *value);
	int32_t    ddobjval_ (int32_t *error, int32_t *diaref, char *name, char *field, int32_t *value, uint64_t lname, uint64_t lfield);
	int32_t    ddopen (int32_t *error, char *exper, char *diag, uint32_t shot, int32_t edition, int32_t *diaref, char *time);
	int32_t    ddopen_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *diaref, char *time, uint64_t lexper, uint64_t ldiag, uint64_t ltime);
	int32_t    ddparm (int32_t *error, int32_t diaref, char *name, char *parm, uint32_t type, uint32_t lbuf, void *buffer, int32_t *physunit);
	int32_t    ddparm_ (int32_t *error, int32_t *diaref, char *name, char *parm, uint32_t *type, uint32_t *lbuf, void *buffer, int32_t *physunit, uint64_t lname, uint64_t lparm);
	void   ddphys_ (int32_t *ier, int32_t *ref, char *name, uint32_t *type, uint32_t *vl, float *pdat, float *fmin, float *fmax, char *physdim, uint64_t lname, uint64_t lphysdim);
	int32_t    ddprinfo (int32_t *error, int32_t diaref, char *name, int32_t *nrec, char *buffer, uint32_t *items, uint16_t *format, int32_t *devsig);
	int32_t    ddprinfo_ (int32_t *error, int32_t *diaref, char *name, int32_t *nrec, char *buffer, uint32_t *items, uint16_t *format, int32_t *devsig, uint64_t lname);
	int32_t    dd_prinfo (int32_t *error, int32_t diaref, char *name, char *vname, uint32_t *items, uint16_t *format);
	int32_t    dd_prinfo_ (int32_t *error, int32_t *diaref, char *name, char *vname, uint32_t *items, uint16_t *format, uint64_t lname, uint64_t lvname);
	int32_t    ddqget (int32_t *error, int32_t diaref, char *name, int32_t *status, int32_t *lbufq, int32_t *bufferq);
	int32_t    ddqget_ (int32_t *error, int32_t *diaref, char *name, int32_t *status, int32_t *lbufq, int32_t *bufferq, uint64_t lname);
	int32_t    ddqinfo (int32_t *error, int32_t diaref, char *name, int32_t *exist, uint32_t *indices, uint32_t *maxsection);
	int32_t    ddqinfo_ (int32_t *error, int32_t *diaref, char *name, int32_t *exist, uint32_t *indices, uint32_t *maxsection, uint64_t lname);
	int32_t    ddsgroup (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng);
	int32_t    ddsgroup_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, uint64_t lname);
	int32_t    ddshot_prefetch (int32_t *state, char *expers, char *diags, uint32_t *shots, int32_t eds, uint32_t nshot, int32_t wait);
	int32_t    ddshot_prefetch_ (int32_t *state, char *expers, char *diags, uint32_t *shots, int32_t *eds, uint32_t *nshot, int32_t *wait, uint64_t  lexpers, uint64_t ldiags);
	int32_t    ddsignal (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng);
	int32_t    ddsignal_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, uint64_t lname);
	int32_t    ddsinfo (int32_t *error, int32_t diaref, char *name, int32_t *typ, char *tname, uint32_t *ind);
	int32_t    ddsinfo_ (int32_t *error, int32_t *diaref, char *name, int32_t *typ, char *tname, uint32_t *ind, uint64_t lname, uint64_t ltname );
	int32_t    ddtbase (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng);
	int32_t    ddtbase_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, uint64_t lname);
	int32_t    ddtindex (int32_t *error, int32_t diaref, char *name, float time1, float time2, uint32_t *k1, uint32_t *k2);
	int32_t    ddtindex_ (int32_t *error, int32_t *diaref, char *name, float *time1, float *time2, uint32_t *k1, uint32_t *k2, uint64_t lname);
	int32_t    dddtindex (int32_t *error, int32_t diaref, char *name, double time1, double time2, uint32_t *k1, uint32_t *k2);
	int32_t    dddtindex_ (int32_t *error, int32_t *diaref, char *name, double *time1, double *time2, uint32_t *k1, uint32_t *k2, uint64_t lname);
	int32_t    ddtindexneu (int32_t *error, int32_t diaref, char *name, float time1, float time2, uint32_t *k1, uint32_t *k2);
	int32_t    ddtindexneu_ (int32_t *error, int32_t *diaref, char *name, float *time1, float *time2, uint32_t *k1, uint32_t *k2, uint64_t lname);
	int32_t    dddtindexneu (int32_t *error, int32_t diaref, char *name, double time1, double time2, uint32_t *k1, uint32_t *k2);
	int32_t    dddtindexneu_ (int32_t *error, int32_t *diaref, char *name, double *time1, double *time2, uint32_t *k1, uint32_t *k2, uint64_t lname);
	int32_t    ddtmout (int32_t *error, int32_t timeout);
	int32_t    ddtmout_ (int32_t *error, int32_t *timeout);
	int32_t    ddtrange (int32_t *error, int32_t diaref, char *name, float *time1, float *time2, uint32_t *ntval, uint32_t *npretrig);
	int32_t    ddtrange_ (int32_t *error, int32_t *diaref, char *name, float *time1, float *time2, uint32_t *ntval, uint32_t *npretrig, uint64_t lname);
	int32_t    dddtrange (int32_t *error, int32_t diaref, char *name, double *time1, double *time2, uint32_t *ntval, uint32_t *npretrig);
	int32_t    dddtrange_ (int32_t *error, int32_t *diaref, char *name, double *time1, double *time2, uint32_t *ntval, uint32_t *npretrig, uint64_t lname);
	int32_t    dduprmd (int32_t *error, int32_t diaref, char *name, uint32_t type, int32_t lbuf, float *buffer, int32_t *events,
						int32_t *flags, int32_t *mode, uint32_t *leng);
	int32_t    dduprmd_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, int32_t *lbuf, float *buffer, int32_t *events,
				         int32_t *flags, int32_t *mode, uint32_t *leng, uint64_t lname);
	int32_t    dduprot (int32_t *error, int32_t diaref, char *name, uint32_t type, int32_t lbuf, float *buffer, int32_t *events, uint32_t *flags, uint32_t *leng);
	int32_t    dduprot_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, int32_t *lbuf, float *buffer, int32_t *events, uint32_t *flags, uint32_t *leng, uint64_t lname);
	int32_t    ddwait (int32_t *error, uint32_t shot);
	int32_t    ddwait_ (int32_t *error, uint32_t *shot);
	int32_t    ddwaitt (int32_t *error, uint32_t shot, int32_t timeout);
	int32_t    ddwaitt_ (int32_t *error, uint32_t *shot, int32_t *timeout);
	int32_t    ddxtrsignal (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t *indices, uint32_t type, uint32_t lbuf, void *buffer, uint32_t *leng);
	int32_t    ddxtrsignal_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *indices, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *leng, uint64_t lname);
	int32_t    wwainsert (int32_t *error, int32_t diaref, char *name, uint32_t k1, uint32_t k2, uint32_t type, void *buffer, uint32_t *sizes);
	int32_t    wwainsert_ (int32_t *error, int32_t *diaref, char *name, uint32_t *k1, uint32_t *k2, uint32_t *type, void *buffer, uint32_t *sizes, uint64_t lname);
	int32_t    wwclear (int32_t *error, int32_t diaref, char *name);
	int32_t    wwclear_ (int32_t *error, int32_t *diaref, char *name, uint64_t lname);
	int32_t    wwclose (int32_t *error, int32_t diaref, char *disp, char *space);
	int32_t    wwclose_ (int32_t *error, int32_t *diaref, char *disp, char *space, uint64_t ldisp, uint64_t lspace);
	int32_t    wwinsert (int32_t *error, int32_t diaref, char *name, uint32_t type, uint32_t lbuf, void *buffer, uint32_t stride, uint32_t *indices);
	int32_t    wwinsert_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *stride, uint32_t *indices, uint64_t lname);
	int32_t    wwoinfo (int32_t *error, int32_t diaref, char *name, uint32_t *typ, uint16_t *format, uint32_t *leng, uint32_t *items, uint32_t *sizes);
	int32_t    wwoinfo_ (int32_t *error, int32_t *diaref, char *name, uint32_t *typ, uint16_t *format, uint32_t *leng, uint32_t *items, uint32_t *sizes, uint64_t lname);
	int32_t    wwonline (int32_t *error, char *exper, char *diag, int32_t pstatus);
	int32_t    wwonline_ (int32_t *error, char *exper, char *diag, int32_t *pstatus, uint64_t lexper, uint64_t ldiag);
	int32_t    wwopen (int32_t *error, char *exper, char *diag, uint32_t shot, char *mode, int32_t edition, int32_t *diaref, char *time);
	int32_t    wwopen_ (int32_t *error, char *exper, char *diag, uint32_t *shot, char *mode, int32_t *edition, int32_t *diaref,
		            char *time, uint64_t lexper, uint64_t ldiag, uint64_t lmode, uint64_t ltime);
	int32_t    wwparm (int32_t *error, int32_t diaref, char *name, char *parm, uint32_t type, uint32_t lbuf, void *buffer, uint32_t stride);
	int32_t    wwparm_ (int32_t *error, int32_t *diaref, char *name, char *parm, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *stride, uint64_t lname, uint64_t lparm);
	int32_t    wwpred (int32_t *error, int32_t diaref, char *exper, char *diag, uint32_t shot, int32_t edition);
	int32_t    wwpred_ (int32_t *error, int32_t *diaref, char *exper, char *diag, uint32_t *shot, int32_t *edition, uint64_t lexper, uint64_t ldiag);
	int32_t    wwqset (int32_t *error, int32_t diaref, char *name, short status, uint32_t lbufq, int32_t bufferq);
	int32_t    wwqset_ (int32_t *error, int32_t *diaref, char *name, short *status, uint32_t *lbufq, int32_t *bufferq, uint64_t lname);
	int32_t    wwsfile (int32_t *error, int32_t wref, int32_t dref);
	int32_t    wwsfile_ (int32_t *error, int32_t *wref, int32_t *dref);
	int32_t    wwsignal (int32_t *error, int32_t diaref, char *name, uint32_t type, uint32_t lbuf, void *buffer, uint32_t stride);
	int32_t    wwsignal_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *stride, uint64_t lname);
	int32_t    wwtbase (int32_t *error, int32_t diaref, char *name, uint32_t type, uint32_t lbuf, void *buffer, uint32_t stride);
	int32_t    wwtbase_ (int32_t *error, int32_t *diaref, char *name, uint32_t *type, uint32_t *lbuf, void *buffer, uint32_t *stride, uint64_t lname);
	int32_t    wwtext (int32_t *error, int32_t diaref, char *name, char *text);
	int32_t    wwtext_ (int32_t *error, int32_t *diaref, char *name, char *text, uint64_t lname, uint64_t ltext);
	int32_t    xxcom (int32_t error);
	int32_t    xxcom_ (int32_t *error);
	int32_t    xxerrprt (int32_t unit, char *text, int32_t error, uint32_t ctrl, char *ID);
	int32_t    xxerrprt_ (int32_t *unit, char *text, int32_t *error, uint32_t *ctrl, char *ID, uint64_t ltext, uint64_t lID);
	int32_t    xxerror (int32_t error, uint32_t ctrl, char *ID);
	int32_t    xxerror_ (int32_t *error, uint32_t *ctrl, char *ID, uint64_t lID);
	int32_t    xxnote (int32_t error);
	int32_t    xxnote_ (int32_t *error);
	int32_t    xxsev (int32_t error);
	int32_t    xxsev_ (int32_t *error);
	int32_t    xxwarn (int32_t error);
	int32_t    xxwarn_ (int32_t *error);
	void   xxdiaglog_ (char *msg, int32_t wohin);


/* definitions for the current DDB Fortran Library */
	int32_t    ddb_delete_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_time_out, uint64_t lexper, uint64_t  ldiag);
	int32_t    ddb_do_send (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_val1, int32_t *p_val2,
				            int32_t *p_val3, int32_t *p_time_out, char *buffer, int32_t *no_lines, int32_t request, uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_insert_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_time_out, char *buffer,
				       int32_t *no_lines, uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_list_ppred_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_time_out,
		          char *buffer, int32_t *no_lines, uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_list_pred_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_time_out,
		         char *no_lines, int32_t *l_text, uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_list_succ_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_time_out,
		          char *buffer, int32_t *no_lines, uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_mod_quality_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *p_quality,
					         int32_t *p_time_out, uint64_t lexper, uint64_t ldiag);
	int32_t    ddb_mod_status_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *status,
					        int32_t *p_time_out, uint64_t lexper, uint64_t ldiag);
	int32_t    ddb_query_file_ (int32_t *error, char *exper, char *diag, uint32_t *shot, int32_t *edition, int32_t *status,
					        int32_t *p_verification, int32_t *p_quality, int32_t *p_time_out, char *buffer, int32_t *no_lines,
					        uint64_t lexper, uint64_t ldiag, uint64_t  lline);
	int32_t    ddb_query_user_ (int32_t *error, char *exper, char *diag, char *p_user, char *p_capability, int32_t *p_time_out, uint64_t lexper, uint64_t ldiag, uint64_t luser, uint64_t lcap);
	void   ddbgetuid_num_ (int32_t *error, int32_t *num, char *username, uint64_t lusername);

#ifdef __cplusplus
}

#endif

#endif					    /* _DDWWANSIC8_H   */
